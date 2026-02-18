from sqlalchemy import select, delete, update

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import FastAPI, Depends, APIRouter, status, HTTPException

from .db import Graph, User, create_db_and_tables, get_async_sessionmaker

from .user import fastapi_users, auth_backend, current_active_user, get_user_manager, UserManager

from .schema import UserUpdate, UserCreate, UserRead, GraphParams

from contextlib import asynccontextmanager

import uuid

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

router = APIRouter()

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_own_account(user: User = Depends(current_active_user),
                             usermanager: UserManager = Depends(get_user_manager),
                             session: AsyncSession = Depends(get_async_sessionmaker)):

    await session.execute(delete(Graph).where(Graph.user_id == user.id))
    await usermanager.delete(user)
    await session.commit()

app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"])
app.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_reset_password_router(), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_verify_router(UserRead), prefix="/auth", tags=["auth"])
app.include_router(router, prefix="/users", tags=["users"])

app.include_router(fastapi_users.get_users_router(UserRead, UserUpdate), prefix="/users", tags=["users"])
@app.post("/upload")
async def upload_graph(params: GraphParams,
                       user: User = Depends(current_active_user),
                       session: AsyncSession = Depends(get_async_sessionmaker)):
    graph = Graph(
        user_id=user.id,
        title=params.labels["title"],
        graph_type=params.graph_type,
        data={
            "df": params.df,
            "labels": params.labels,
            "checkboxes": params.checkboxes,
            "trendlines": params.trendlines,
            "window_size": params.window_size,
            "previous_lines": params.previous_lines
        }
    )

    session.add(graph)
    await session.commit()
    await session.refresh(graph)

    return graph

@app.get("/feed")
async def get_feed(session: AsyncSession = Depends(get_async_sessionmaker),):

    graphs = await session.execute(select(Graph))
    graphs = graphs.scalars().all()

    graph_data = []
    for graph in graphs:
        graph_data.append({
            "id": graph.id,
            "user_id": graph.user_id,
            "title": graph.title,
            "graph_type": graph.graph_type,
            "data": graph.data,
            "created_at": graph.created_at

        })

    return graph_data


@app.get("/user/graphs")
async def get_user_graph(user: User = Depends(current_active_user),
                   session: AsyncSession = Depends(get_async_sessionmaker)):

    graphs = await session.execute(select(Graph).where(Graph.user_id == user.id))
    graphs = graphs.scalars().all()
    graph_data = []
    for graph in graphs:
        graph_data.append({
            "id": graph.id,
            "user_id": graph.user_id,
            "title": graph.title,
            "graph_type": graph.graph_type,
            "data": graph.data,
            "created_at": graph.created_at
        })

    return graph_data


@app.delete("/graph/{graph_id}")
async def delete_graph(graph_id: uuid.UUID,
                 session: AsyncSession = Depends(get_async_sessionmaker),
                 ):
    await session.execute(delete(Graph).where(Graph.id == graph_id))
    await session.commit()
@app.api_route("/health", methods=["GET", "HEAD"])
async def health_check():
    return {"status": "ok"}

@app.get("/user/update/{graph_id}")
async def get_update_graph(graph_id: uuid.UUID,
                           user: User = Depends(current_active_user),
                           session: AsyncSession = Depends(get_async_sessionmaker)):
    uuids = await session.execute(select(Graph).where(Graph.id == graph_id and Graph.user_id == user.id))
    uuids = uuids.scalars().all()
    uuids = [graph.id for graph in uuids]
    if graph_id not in uuids:
        raise HTTPException(status_code=404, detail="Graph not found")

    else:
        graph = await session.execute(select(Graph).where(Graph.id == graph_id and Graph.user_id == user.id))
        graph = graph.scalars().all()
        graph_data = None
        for graph in graph:
            graph_data = {
                "id": graph.id,
                "user_id": graph.user_id,
                "title": graph.title,
                "graph_type": graph.graph_type,
                "data": graph.data,
                "created_at": graph.created_at
            }

        return graph_data

@app.put("/graph/update/{graph_id}")
async def update_graph(graph_id: uuid.UUID,
                       params: GraphParams,
                       session: AsyncSession = Depends(get_async_sessionmaker),
                       user: User = Depends(current_active_user)
                       ):
    updated_graph = await session.execute(
        update(Graph)
        .where(Graph.id == graph_id and Graph.user_id == user.id)
        .values(title=params.labels["title"],
                graph_type=params.graph_type,
                data={
            "df": params.df,
            "labels": params.labels,
            "checkboxes": params.checkboxes,
            "trendlines": params.trendlines,
            "window_size": params.window_size,
            "previous_lines": params.previous_lines
        })
    )

    await session.commit()
    return updated_graph

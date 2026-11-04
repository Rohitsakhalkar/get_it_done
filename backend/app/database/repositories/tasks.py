from app.schemas.tasks import CreateTask, ShowTask, UpdateTask
from app.database.models import Task, User
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

def create_task(task: CreateTask, db, current_user):
    db_task = Task(
        user_id = current_user.id,
        title = task.title,
        description = task.description,
        location = task.location,
        payment = task.payment 
    )
    db.add(db_task)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code = 422, detail = "couldn't update task")
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code = 500, detail = "Couldn't create task")
    db.refresh(db_task)
    response = ShowTask(
        id = db_task.id,
        title = db_task.title,
        description = db_task.description,
        name = current_user.name,
        username = current_user.username,
        location = db_task.location,
        payment = db_task.payment,
        status = db_task.status,
        created_at = db_task.created_at,
        updated_at = db_task.updated_at
    )
    return response

def show_tasks(location, current_user, db, limit, offset):
    if location is None:
        location = current_user.work_location
    result = db.query(Task, User).join(User, User.id == Task.user_id).filter(Task.location.ilike(
        f"%{location}%")).order_by(Task.id.desc()).limit(limit).offset(offset).all() 
    tasks_list = []
    for task, user in result:
        response = ShowTask(
            id = task.id,
            title = task.title,
            description = task.description,
            name = user.name,
            username = user.username,
            location = task.location,
            payment = task.payment,
            status = task.status,
            created_at = task.created_at,
            updated_at = task.updated_at
        )
        tasks_list.append(response)
    return tasks_list

def update_task(task_id, details: UpdateTask, db, current_user):
    updates = details.model_dump(exclude_unset = True)
    if not updates:
        raise HTTPException(status_code = 400, detail = "empty json")
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None: 
        raise HTTPException(status_code = 404, detail = "task doesn't exist")
    if current_user.id != task.user_id:
        raise HTTPException(status_code = 403, detail = "unauthorized user") 
    if task.status == "open":
        for field,value in updates.items():
            setattr(task, field, value)
    else:
        raise HTTPException(status_code = 409, detail = "task already assigned to someone cannot change the details")
    try: 
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code = 422, detail = "couldn't update task")
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code = 500, detail = "couldn't update task")
    response = ShowTask(
            id = task.id,
            title = task.title,
            description = task.description,
            username = current_user.username,
            name = current_user.name,
            location = task.location,
            payment = task.payment,
            status = task.status,
            created_at = task.created_at,
            updated_at = task.updated_at 
        ) 
    return response

def show_task(task_id, db):
    result = db.query(Task, User).join(User, User.id == Task.user_id).filter(Task.id == task_id).first()
    if result is None:
        raise HTTPException(status_code = 404, detail = "task not found")
    task, user = result
    response = ShowTask(
        id = task.id,
        title = task.title,
        description = task.description,
        username = user.username,
        name = user.name,
        location = task.location,
        payment = task.payment,
        status = task.status,
        created_at = task.created_at,
        updated_at = task.updated_at 
    ) 
    return response
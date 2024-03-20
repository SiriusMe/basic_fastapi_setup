from ... import models, schemas
from ... import oauth2
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['posts']
)


# CRUD operations for posts

# CREATING
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.GetPost)
def create_post(post: schemas.CreatePost, db: Session = Depends(get_db),
                user_id: int = Depends(oauth2.get_current_user)):
    """
    #post as dict
    post_dict =post.dict()
    #creating id 
    post_dict['id'] = randrange(0,1000)
    #adding the new post to the array
    my_posts.append(post_dict)
  """

    # creating the post with raw sql cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s,
    # %s) RETURNING * """,(post.title, post.content, post.published)) new_post= cursor.fetchone() conn.commit()
    print(user_id)
    new_post = models.Post(**post.dict())
    # new_post = models.Post(title=post.title, content=post.content, published= post.published)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    created_at = new_post.created_at
    # response_post = {
    #     "id": new_post.id,
    #     "title": new_post.title,
    #     "content": new_post.content,
    #     "published": new_post.published,
    #     "created_at": new_post.created_at,
    # }

    return {
        "id": new_post.id,
        "title": new_post.title,
        "content": new_post.content,
        "created_at": created_at}


# RETRIVING
@router.get("/{id}")
def root(id: int, db: Session = Depends(get_db)):
    #    cursor.execute("""SELECT * FROM posts where id=%s""",(str(id)))
    #    post= cursor.fetchone()

    # post = find_post(id)

    post = db.query(models.Post).filter(models.Post.id == id).first()

    # if not found
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the post with id:{id} not found")
    #    if post:
    #     post_dict = post.__dict__
    #     # Removing internal SQLAlchemy-related attributes
    #     post_dict.pop("_sa_instance_state", None)
    #    else:
    #         # Handle the case when no post with the given id is found
    #         post_dict = {}

    # if found
    print("=======================")
    print(post)
    print("=======================")
    return post


# DELETING
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # finding the index in the array that has required ID
    # my_post.pop(index)

    # cursor.execute("""DELETE FROM posts WHERE id=%s returning * """,(str(id)))
    # delete_post = cursor.fetchone()
    # conn.commit()
    # index = find_index_post(id)
    print(user_id)
    post = db.query(models.Post).filter(models.Post.id == id)

    # if not found
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} does not exsist")

    # my_posts.pop(delete_post)

    # if found
    post.delete(synchronize_session=False)
    db.commit()
    return {'message': 'post was deleted'}


# updating post
@router.put("/{id}")
def update_post(id: int, post: schemas.UpdatePost, db: Session = Depends(get_db)):
    # cursor.execute("""update posts set title=%s, content=%s, published=%s where id=%s returning * """,(post.title,
    # post.content, post.published, str(id))) updated_post = cursor.fetchone() conn.commit() index = find_index_post(
    # id)

    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()

    # if not found
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} does not exsist")

    # if found
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return {"updated_post_is ": post_query.first()}


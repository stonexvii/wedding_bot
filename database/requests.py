from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .database import connection
from .tables import AnswersTable, UserAnswers, QuestionsTable


@connection
async def add_question(question: str, session: AsyncSession):
    session.add(QuestionsTable(question=question))
    await session.commit()


@connection
async def add_answer(question_id: int, answer_id: int, answer: str, session: AsyncSession):
    session.add(AnswersTable(
        question_id=question_id,
        answer_id=answer_id,
        answer=answer,
    ))
    await session.commit()


@connection
async def get_question(question_id: int, session: AsyncSession):
    question = await session.scalar(select(QuestionsTable).where(QuestionsTable.id == question_id))
    if question:
        answers = await session.scalars(
            select(AnswersTable).where(AnswersTable.question_id == question_id))
        return question, answers.all()


@connection
async def next_user_question_id(user_id: int, session: AsyncSession):
    response = await session.scalars(select(UserAnswers.question_id).where(UserAnswers.user_id == user_id))
    response = response.all()
    return max(response) + 1 if response else 1


@connection
async def add_user_answer(user_id: int, question_id: int, answer_id: int, session: AsyncSession):
    session.add(UserAnswers(
        user_id=user_id,
        question_id=question_id,
        answer_id=answer_id,
    ))
    await session.commit()


@connection
async def all_questions(session: AsyncSession):
    response = await session.scalars(select(QuestionsTable))
    return response.all()


@connection
async def all_answers(session: AsyncSession):
    response = await session.scalars(select(UserAnswers))
    return response.all()

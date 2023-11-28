from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from src.bot.fsm import RecordGroup
from src.bot.handlers.record.get import back
from src.bot.keyboards.service import YESNO_KB
from src.db import Database

router = Router()


@router.callback_query(F.data == 'delete_record', RecordGroup.viewing_record)
async def delete_record_question(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.message.answer(
        'Вы действительно хотите удалить запись? Все данные, содержащиеся в ней, будут безвозвратно потеряны.',
        reply_markup=YESNO_KB
    )
    await state.set_state(RecordGroup.deleting_record)
    await call.answer()


@router.callback_query(F.data == 'yes', RecordGroup.deleting_record)
async def delete_record_yes(call: types.CallbackQuery, state: FSMContext, db: Database) -> None:
    user_data = await state.get_data()

    async with db.session.begin():
        record = await db.record.get(user_data['record_id'])
        await db.record.delete(record)

    await call.message.answer('Запись успешно удалена ✅')
    await back(call, state, db)
    await call.answer()


@router.callback_query(F.data == 'no', RecordGroup.deleting_record)
async def delete_record_no(call: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(RecordGroup.viewing_record)
    await call.message.answer('Удаление записи отменено ❌')
    await call.answer()

async def send_message_by_type(bot, user_telegram_id, message, text):
    if message.text:
        await bot.send_message(user_telegram_id, text + "\n" + message.text)
    elif message.sticker:
        await bot.send_message(user_telegram_id, text)
        await bot.send_sticker(user_telegram_id, message.sticker.file_id)
    elif message.photo:
        photos = list(sorted(message.photo, key=lambda photo: photo.file_size))
        await bot.send_message(user_telegram_id, text)
        await bot.send_photo(user_telegram_id, photos[0].file_id)
    elif message.document:
        await bot.send_message(user_telegram_id, text)
        await bot.send_document(user_telegram_id, message.document.file_id)
    elif message.audio:
        await bot.send_message(user_telegram_id, text)
        await bot.send_audio(user_telegram_id, message.audio.file_id)
    elif message.video:
        await bot.send_message(user_telegram_id, text)
        await bot.send_video(user_telegram_id, message.video.file_id)
    elif message.video_note:
        await bot.send_message(user_telegram_id, text)
        await bot.send_video_note(user_telegram_id, message.video_note.file_id)
    elif message.voice:
        await bot.send_message(user_telegram_id, text)
        await bot.send_voice(user_telegram_id, message.voice.file_id)
    else:
        raise Exception("Неизвестный тип сообщения, попробуйте ещё раз")
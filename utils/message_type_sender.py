async def send_message_by_type(bot, user_telegram_id, message, text):
    if message.text:
        await bot.send_message(user_telegram_id, text + "\n" + message.text)
        return (message.text, 'text')
    elif message.sticker:
        await bot.send_message(user_telegram_id, text)
        await bot.send_sticker(user_telegram_id, message.sticker.file_id)
        file = await bot.get_file(message.sticker.file_id)
        return (file.file_path, 'sticker')
    elif message.photo:
        photos = list(sorted(message.photo, key=lambda photo: photo.file_size))
        await bot.send_message(user_telegram_id, text)
        await bot.send_photo(user_telegram_id, photos[0].file_id)
        file = await bot.get_file(photos[0].file_id)
        return (file.file_path, 'photo')
    elif message.document:
        await bot.send_message(user_telegram_id, text)
        await bot.send_document(user_telegram_id, message.document.file_id)
        file = await bot.get_file(message.document.file_id)
        return (file.file_path, 'document')
    elif message.audio:
        await bot.send_message(user_telegram_id, text)
        await bot.send_audio(user_telegram_id, message.audio.file_id)
        file = await bot.get_file(message.audio.file_id)
        return (file.file_path, 'audio')
    elif message.video:
        await bot.send_message(user_telegram_id, text)
        await bot.send_video(user_telegram_id, message.video.file_id)
        file = await bot.get_file(message.video.file_id)
        return (file.file_path, 'video')
    elif message.video_note:
        await bot.send_message(user_telegram_id, text)
        await bot.send_video_note(user_telegram_id, message.video_note.file_id)
        file = await bot.get_file(message.video_note.file_id)
        return (file.file_path, 'video_note')
    elif message.voice:
        await bot.send_message(user_telegram_id, text)
        await bot.send_voice(user_telegram_id, message.voice.file_id)
        file = await bot.get_file(message.voice.file_id)
        return (file.file_path, 'voice')
    else:
        raise Exception("Неизвестный тип сообщения, попробуйте ещё раз")
import discord
from discord.ext import commands
import random
import time
from discord import Intents

class CustomQueue:
    def __init__(self):
        self.queue = []

    def enqueue(self, message):
        self.queue.append(message)

    def dequeue(self):
        if self.is_empty():
            raise Exception("Queue is empty")
        return self.queue.pop(0)

    def is_empty(self):
        return len(self.queue) == 0

    def size(self):
        return len(self.queue)

class CustomStack:
    def __init__(self):
        self.stack = []

    def push(self, message):
        self.stack.append(message)

    def pop(self):
        if self.is_empty():
            raise Exception("Stack is empty")
        return self.stack.pop()

    def is_empty(self):
        return len(self.stack) == 0

    def size(self):
        return len(self.stack)

intents = discord.Intents.default()
intents.typing = True
intents.presences = True
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

queue = CustomQueue()
stack = CustomStack()


class CustomQueue:
    def __init__(self):
        self.queue = []

    def enqueue(self, item):
        self.queue.insert(0, item)

    def dequeue(self):
        if self.is_empty():
            raise Exception("Queue is empty")
        return self.queue.pop()

    def is_empty(self):
        return len(self.queue) == 0

    def size(self):
        return len(self.queue)


class CustomStack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if self.is_empty():
            raise Exception("Stack is empty")
        return self.stack.pop()

    def is_empty(self):
        return len(self.stack) == 0

    def size(self):
        return len(self.stack)


# Đẩy nội dung từ messager_auto.txt vào queue
with open("messager_auto.txt", "r", encoding="utf-8") as auto_file:
    for line in auto_file:
        line = line.strip()
        queue.enqueue(line)


@bot.command(name='enqueue')
async def enqueue_message(ctx, *, message):
    if len(message) > 255:
        await ctx.send("Câu hỏi quá dài. Vui lòng nhập câu hỏi ngắn hơn.")
        return
    queue.enqueue(message)
    await ctx.send(f'Message "{message}" has been enqueued.')


@bot.command(name='dequeue')
async def dequeue_message(ctx):
    try:
        message = queue.dequeue()
        await ctx.send(f'Dequeued message: {message}')
    except Exception as e:
        await ctx.send(str(e))


@bot.command(name='push')
async def push_message(ctx, *, message):
    if len(message) > 255:
        await ctx.send("Câu hỏi quá dài. Vui lòng nhập câu hỏi ngắn hơn.")
        return
    else:
        stack.push(message)
        await ctx.send(f'Message "{message}" has been pushed to the stack.')


@bot.command(name='pop')
async def pop_message(ctx):
    try:
        message = stack.pop()
        await ctx.send(f'Popped message: {message}')
    except Exception as e:
        await ctx.send(str(e))


@bot.command(name='chat')
async def chat(ctx):
    startedSAnswer = time.time()
    user_message = ctx.message.content.replace("/chat", "").strip()
    user_questions = user_message.split("?")
    for question in user_questions:
        if question.strip() and len(question) <= 255:
            stack.push(question.strip())
        elif len(question) > 255:
            await ctx.send("Câu hỏi quá dài. Vui lòng nhập câu hỏi ngắn hơn.")
            break
    while not stack.is_empty():
        if not queue.is_empty():
            stacked_message = stack.pop()
            queue_message = queue.dequeue()
            time_ms = round(time.time() - startedSAnswer)* 100
            await ctx.send(f' **Question:** {stacked_message} \n**Answer:** {queue_message}\n---------{time_ms:.2f}ms----------')
        else:
            time_ms = round(time.time() - startedSAnswer) * 100
            stacked_message = stack.pop()
            await ctx.send(f'Vui lòng đợi admin thêm câu trả lời.\n---------{time_ms:.2f}ms----------')


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


bot.run('BOT_TOKEN')

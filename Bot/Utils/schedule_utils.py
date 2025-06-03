from .constants import schedule, times, all_lessons, days

async def add_lesson(day, time, lesson):
    if lesson == 'Командно-лидерские турниры':
        schedule[days[day]][times[0]] = lesson
        for i in range(1,13):
            del schedule[days[day]][times[i]]
    elif lesson in ['Практические занятие/стажировка', 'Теоретическое занятие', 'Занятие с инженерами-наставниками']:
        current_index = times.index(time)
        for i in range(current_index, current_index + 4):
            schedule[days[day]][times[i]] = lesson
    else:
        current_index = times.index(time)
        for i in range(current_index, current_index + 6):
            schedule[days[day]][times[i]] = lesson

def check_lesson_count(shedule, lesson_name):
    count = 0
    for day, lessons in shedule.items():
        for time, subject in lessons.items():
            if subject == lesson_name:
                count += 1
    return count

def lesson_count(shedule):
    count = 0
    for i in all_lessons:
        for day, lessons in shedule.items():
            for time, subject in lessons.items():
                if subject == i:
                    count += 1
    return count

def day_schedule(schedule, day):
    day_schedule = f'{day}:\n'
    for time in times:
        try:
            event = schedule[day][time]
            if event == 'Командно-лидерские турниры':
                day_schedule += f'8:00 - 20:00: {event}\n'
            else:
                day_schedule += f'{time}: {event}\n'
        except: 
            continue
    return day_schedule
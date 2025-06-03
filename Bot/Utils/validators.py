from .constants import times, all_lessons, days

def check_time_for_lesson(shedule, lesson_name, time_start, day):
    time = int(time_start.split(':')[0])
    current_index = times.index(time_start)
    count = 0
    error = 'Неизвестная ошибка'
    flag = True
    if lesson_name == 'Практические занятие/стажировка' or lesson_name == 'Теоретическое занятие' or lesson_name == 'Занятие с инженерами-наставниками': count = 4
    elif lesson_name == 'Смежные компетенции': count = 6
    else: count = 12
    if lesson_name == 'Практические занятие/стажировка' or lesson_name == 'Теоретическое занятие' or lesson_name == 'Занятие с инженерами-наставниками':
        if time < 18:
            current_index = times.index(time_start)
            for item in all_lessons:
                for i in range(current_index, current_index+4):
                    if item == shedule[days[day]][times[i]]:
                        flag = False
                        error = 'Выбранный предмет пересекается с другим предметом, попробуйте поставить в другое время или день.'
                        break 
                if flag == False:
                    break
            return flag, error
        else:
            flag = False
            error = 'Вы не входите во временные рамки, выберите другое время или день'
            return flag, error
    elif lesson_name == 'Смежные компетенции':
        current_index = times.index(time_start)
        if time < 16:
            for item in all_lessons:
                for i in range(current_index, current_index+count):
                    if item == shedule[days[day]][times[i]]:
                        flag = False
                        error = 'Выбранный предмет пересекается с другим предметом, попробуйте поставить в другое время или день.'
                        break
                if not flag:
                    break
            return flag, error
        else: 
            flag = False
            error = 'Вы не входите во временные рамки, выберите другое время или день'
            return flag, error
    elif lesson_name == 'Командно-лидерские турниры':
        for item in all_lessons:
            for i in range(0, 11):
                if item == shedule[days[day]][times[i]]:
                    flag = False
                    error = 'Выбранный предмет пересекается с другим предметом, попробуйте поставить в другое время или день.'
                    break
            if not flag:
                break
        return flag, error
    return flag
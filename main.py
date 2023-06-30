import csv
import re

FILE_PATH = 'phonebook_raw.csv'
OUTPUT_PATH = 'output.csv'


def read_csv():
    with open(FILE_PATH) as file:
        reader = csv.DictReader(file)
        return list(reader)


def write_csv(path, to_output):
    with open(path, 'w', encoding='utf-8') as output:
        fieldnames = ['lastname', 'firstname', 'surname', 'organization', 'position', 'phone', 'email', 'key']
        selected_fieldnames = ['lastname', 'firstname', 'surname', 'organization', 'position', 'phone', 'email']
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        for row in to_output:
            filtered_row = {key: row[key] for key in selected_fieldnames}
            writer.writerow(filtered_row)
    print('Reformationg complite!')


def reform(input):
    result = []
    keys = []

    for line in input:
        key = line['lastname'].strip() + ' ' + line['firstname'].strip() + ' ' + line['surname'].strip()
        if key.strip() in keys:
            for searched_line in result:
                if searched_line['key'] == key:
                    if not searched_line['organization']:
                        searched_line['organization'] = line['organization']
                    if not searched_line['position']:
                        searched_line['position'] = line['position']
                    if not searched_line['email']:
                        searched_line['email'] = line['email']

        else:
            new_line = {}
            new_line['key'] = key.strip()
            fio = key.split(' ')
            match len(fio):
                case 1:
                    new_line['lastname'] = ''
                    new_line['firstname'] = fio[0]
                    new_line['surname'] = ''
                case 2:
                    new_line['lastname'] = fio[0]
                    new_line['firstname'] = fio[1]
                    new_line['surname'] = ''
                case 3:
                    new_line['lastname'] = fio[0]
                    new_line['firstname'] = fio[1]
                    new_line['surname'] = fio[2]
                case _:
                    new_line['lastname'] = fio[0]
                    new_line['firstname'] = fio[1]
                    new_line['surname'] = ' '.join(fio[2:])

            new_line['organization'] = line['organization'] or ''
            new_line['position'] = line['position'] or ''
            new_line['email'] = line['email'] or ''

            delete_digits_pattern = r'[\D]*'
            formated_phone = re.sub(delete_digits_pattern, '', line['phone'])
            match len(formated_phone):
                case 0:
                    new_line[
                        'phone'] = ''
                case 11:
                    new_line[
                        'phone'] = f'+7({formated_phone[1:4]})-{formated_phone[4:7]}-{formated_phone[7:9]}-{formated_phone[9:]}'
                case 10:
                    new_line[
                        'phone'] = f'+7({formated_phone[0:3]})-{formated_phone[3:6]}-{formated_phone[6:9]}-{formated_phone[9:]}'
                case _:
                    new_line[
                        'phone'] = f'+7({formated_phone[0:3]})-{formated_phone[3:6]}-{formated_phone[6:9]}-{formated_phone[9:11]} доп. {formated_phone[11:]} '

            result.append(new_line)
            keys.append(key.strip())

    return result


def main():
    input = read_csv()
    output = reform(input)
    write_csv(OUTPUT_PATH, output)


if __name__ == '__main__':
    main()

import xlsx from 'xlsx';

const convert_tenants_to_array = (data) => { // Сделать из колонки со студентами массив
  for(let row of data) { // Перебрать строки колонки таблицы
    try {
      const tenants = row['Проживающие'].split('\n') // Разбиваем строку со студентами в массив
      row['Проживающие'] = tenants; // Присваиваем массив вместо строки
    } catch(err) {
      if(err instanceof TypeError) { // Если в строке пусто, идем дальше
        continue
      }
    }
  };
};

const convert_tenants_to_string = (data) => {
  for(let row of data) { // Перебрать строки колонки таблицы
    try {
      const tenants = row['Проживающие'].join('\n') // собираем массив со студентами в строку
      row['Проживающие'] = tenants; // Присваиваем строку вместо массива
    } catch(err) {
      console.log(err);
    }
  };
};

const delete_trash_data = (data) => {
  const new_data = [];
  for(let i of data) {
    new_data.push({
      '№ ком.': i['№ ком.'],
      'Проживающие': i['Проживающие']
    });
  };
  return new_data
};

const find_faculty_students = (data, faculty_name) => { // найти студентов конкретного факультета
  const new_data = [];
  for(let i of data) {
    const new_tenants = []; // Массив с нужными студентами

    try {
      for(let tenant of i['Проживающие']) { // Перебираем массив со студентами и ищем нужных, добавляем их в новый массив
        if(tenant.indexOf(faculty_name) != -1) {
          new_tenants.push(tenant);
        }
      };

      if(new_tenants.length == 0) { // Если в комнате нет нужных студентов, пропускаем ее
        continue
      };

      i['Проживающие'] = new_tenants; // Присваиваем новый массив вместо старого
      new_data.push(i)

    } catch(err) {
      if(err instanceof ReferenceError) {
        continue
      }
    }
  };
  return new_data;
};

const get_students_for_faculties = (workbook, faculty_name) => {
  convert_tenants_to_array(data);
  let prepared_data = find_faculty_students(data, faculty_name);
  convert_tenants_to_string(prepared_data);
  prepared_data = delete_trash_data(prepared_data);

  const worksheet = xlsx.utils.json_to_sheet(prepared_data);
  xlsx.utils.book_append_sheet(workbook, worksheet, faculty_name);
};

const file = xlsx.readFile('infile_prepared.xlsx');
const sheets = file.SheetNames;
const data = xlsx.utils.sheet_to_json(file.Sheets[sheets[0]]);

const faculty_names = [ // Названия факультетов чтобы не писать вручную
  'ФВМиЗ',
  'ФЭИТ',
  'ФЗКиСТ',
  'ФАиЛХ',
  'ИФ'
];


const workbook = xlsx.utils.book_new();

for(const i of faculty_names) {
  get_students_for_faculties(workbook,i);
};

xlsx.writeFile(workbook, `Студенты в общежитии по факультетам.xlsx`);

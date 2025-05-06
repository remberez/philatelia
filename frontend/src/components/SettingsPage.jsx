import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import userStore from '../stores/userStore';
import { observer } from 'mobx-react-lite';
import userService from '../services/userService';
import { toJS } from 'mobx';
import { useState } from 'react';

const SettingsPage = observer(() => {
    const user = toJS(userStore.user);
    const [isSuccess, setIsSuccess] = useState(false);
  
    const validationSchema = Yup.object({
      username: Yup.string().required('Имя пользователя обязательно'),
      email: Yup.string().email('Неверный email').required('Email обязателен'),
      password: Yup.string().min(6, 'Минимум 6 символов'),
    });
  
    const handleSubmit = async (values) => {
      const response = await userService.updateMe(values);
      if (response) {
        setIsSuccess(true);
      }
    };
  
    if (!user || !user.username || !user.email) {
      return <div className="text-center text-gray-600">Загрузка данных...</div>;
    }
  
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
        <div className="bg-white shadow-md rounded-2xl p-6 w-full max-w-md">
            <div className="flex items-center gap-x-4 mb-4">
                <h1 className="text-2xl font-semibold text-gray-800">Настройки</h1>
                { isSuccess && <div className="text-green-500">Данные успешно обнавлены</div>}
            </div>
          <Formik
            initialValues={{ ...user, password: '' }} // обязательно добавь password
            enableReinitialize
            validationSchema={validationSchema}
            onSubmit={handleSubmit}
          >
            <Form className="space-y-4">
              <div>
                <label className="block text-sm text-gray-600 mb-1" htmlFor="username">Имя пользователя</label>
                <Field
                  name="username"
                  type="text"
                  className="w-full border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <ErrorMessage name="username" component="div" className="text-red-500 text-sm mt-1" />
              </div>
  
              <div>
                <label className="block text-sm text-gray-600 mb-1" htmlFor="email">Email</label>
                <Field
                  name="email"
                  type="email"
                  className="w-full border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <ErrorMessage name="email" component="div" className="text-red-500 text-sm mt-1" />
              </div>
  
              <div>
                <label className="block text-sm text-gray-600 mb-1" htmlFor="password">Пароль</label>
                <Field
                  name="password"
                  type="password"
                  className="w-full border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <ErrorMessage name="password" component="div" className="text-red-500 text-sm mt-1" />
              </div>
  
              <button
                type="submit"
                className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 transition"
              >
                Сохранить изменения
              </button>
            </Form>
          </Formik>
        </div>
      </div>
    );
  });
  
  export default SettingsPage;

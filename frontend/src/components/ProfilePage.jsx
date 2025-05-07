import { observer } from "mobx-react-lite";
import userStore from "../stores/userStore";
import { Link } from "react-router-dom";

const ProfilePage = () => {
    const user = userStore.user || {};
  
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
        <div className="bg-white shadow-md rounded-2xl p-6 max-w-md w-full">
          <h1 className="text-2xl font-semibold mb-4 text-gray-800">Профиль пользователя</h1>
          <div className="space-y-3">
            <div>
              <p className="text-gray-500 text-sm">ID</p>
              <p className="text-gray-800 font-medium">{user.id}</p>
            </div>
            <div>
              <p className="text-gray-500 text-sm">Имя пользователя</p>
              <p className="text-gray-800 font-medium">{user.username}</p>
            </div>
            <div>
              <p className="text-gray-500 text-sm">Email</p>
              <p className="text-gray-800 font-medium">{user.email}</p>
            </div>
            <div>
              <p className="text-gray-500 text-sm">Роль</p>
              <p className="text-gray-800 font-medium">{user.role}</p>
            </div>
            <Link to={"/my-groups"} className="bg-green-500 px-4 py-2 text-white text-sm block text-center rounded-lg hover:bg-green-600">
              Мои группы
            </Link>
          </div>
        </div>
      </div>
    );
  };
  
  export default observer(ProfilePage);
  
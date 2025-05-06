import { Outlet, Link } from "react-router-dom";
import { useState } from "react";

const MainLayout = () => {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  const toggleDropdown = () => {
    setIsDropdownOpen((prev) => !prev);
  };

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <header className="bg-blue-600 text-white p-4 shadow-lg">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <h1 className="text-3xl font-semibold">Philatelist Club</h1>
            <nav className="hidden md:flex space-x-6 ml-10">
              <Link to="/" className="text-lg hover:text-gray-300">
                Главная
              </Link>
              <Link to="/about" className="text-lg hover:text-gray-300">
                О нас
              </Link>
              <Link to="/club" className="text-lg hover:text-gray-300">
                Клубы
              </Link>
            </nav>
          </div>
          
          <div className="relative">
            <button
              onClick={toggleDropdown}
              className="flex items-center space-x-2 px-4 py-2 bg-blue-700 rounded-full hover:bg-blue-800"
            >
              <span>Профиль</span>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                className="w-5 h-5"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M19 9l-7 7-7-7"
                />
              </svg>
            </button>
            
            {isDropdownOpen && (
              <div className="absolute right-0 mt-2 w-48 bg-white border border-gray-200 rounded-md shadow-lg">
                <div className="py-2">
                  <Link
                    to="/profile"
                    className="block px-4 py-2 text-gray-700 hover:bg-gray-100"
                  >
                    Открыть профиль
                  </Link>
                  <Link
                    to="/settings"
                    className="block px-4 py-2 text-gray-700 hover:bg-gray-100"
                  >
                    Настройки
                  </Link>
                  <button
                    className="block w-full px-4 py-2 text-left text-gray-700 hover:bg-gray-100"
                    onClick={() => {
                      // Handle logout
                      console.log("Logged out");
                    }}
                  >
                    Выйти
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </header>

      <main className="flex-grow p-4">
        <Outlet />
      </main>

      <footer className="bg-blue-600 text-white p-4 text-center">
        &copy; 2025 Philatelist Club
      </footer>
    </div>
  );
};

export default MainLayout;

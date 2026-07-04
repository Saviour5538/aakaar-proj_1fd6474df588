import axios, { AxiosInstance } from 'axios';

const api: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '',
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface Task {
  id: number;
  title: string;
  description: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

export interface CreateTaskRequest {
  title: string;
  description: string;
  completed: boolean;
}

export interface UpdateTaskRequest {
  title?: string;
  description?: string;
  completed?: boolean;
}

export const register = (data: RegisterRequest) => api.post<TokenResponse>('/api/auth/register', data);

export const login = (data: LoginRequest) => api.post<TokenResponse>('/api/auth/login', data);

export const createTask = (data: CreateTaskRequest) => api.post<Task>('/api/tasks', data);

export const listTasks = () => api.get<Task[]>('/api/tasks');

export const updateTask = (id: number, data: UpdateTaskRequest) => api.put<Task>(`/api/tasks/${id}`, data);

export const deleteTask = (id: number) => api.delete<void>(`/api/tasks/${id}`);

export default api;

// Auto-added stubs for functions a page imported but the client omitted.
export const getTask = async (id: string) => {
  const res = await api.get(`/api/tasks/${id}`);
  return res.data;
};

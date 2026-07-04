import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { createTask, updateTask, getTask } from '../api/client';

interface TaskFormValues {
  title: string;
  description: string;
  completed: boolean;
}

const TasksForm: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [formValues, setFormValues] = useState<TaskFormValues>({
    title: '',
    description: '',
    completed: false,
  });
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (id) {
      const fetchTask = async () => {
        setLoading(true);
        setError(null);
        try {
          const task = await getTask(Number(id));
          setFormValues({
            title: task.title,
            description: task.description,
            completed: task.completed,
          });
        } catch (err) {
          setError('Failed to fetch task.');
        } finally {
          setLoading(false);
        }
      };

      fetchTask();
    }
  }, [id]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value, type, checked } = e.target;
    setFormValues((prevValues) => ({
      ...prevValues,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      if (id) {
        await updateTask(Number(id), formValues);
      } else {
        await createTask(formValues);
      }
      navigate('/tasks');
    } catch (err) {
      setError('Failed to save task.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">{id ? 'Edit Task' : 'Create Task'}</h1>
      {loading && <div className="text-center">Loading...</div>}
      {error && <div className="text-red-500 mb-4">{error}</div>}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-1">Title</label>
          <input
            type="text"
            name="title"
            value={formValues.title}
            onChange={handleChange}
            className="w-full p-2 border border-gray-300 rounded"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Description</label>
          <textarea
            name="description"
            value={formValues.description}
            onChange={handleChange}
            className="w-full p-2 border border-gray-300 rounded"
            required
          />
        </div>
        <div>
          <label className="flex items-center">
            <input
              type="checkbox"
              name="completed"
              checked={formValues.completed}
              onChange={handleChange}
              className="mr-2"
            />
            Completed
          </label>
        </div>
        <div className="flex justify-end">
          <button
            type="submit"
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
          >
            Save
          </button>
        </div>
      </form>
    </div>
  );
};

export default TasksForm;
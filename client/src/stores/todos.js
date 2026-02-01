import { writable } from 'svelte/store';
import axios from 'axios';

const API_URL = '/api/todos';

// Create a writable store for todos
export const todos = writable([]);
export const loading = writable(false);
export const error = writable(null);

// Fetch all todos
export async function fetchTodos() {
    loading.set(true);
    error.set(null);
    try {
        const response = await axios.get(API_URL);
        todos.set(response.data);
    } catch (err) {
        error.set(err.message);
        console.error('Error fetching todos:', err);
    } finally {
        loading.set(false);
    }
}

// Add a new todo
export async function addTodo(title, description = '') {
    try {
        const response = await axios.post(API_URL, {
            title,
            description,
            completed: false
        });
        todos.update(t => [...t, response.data]);
        return response.data;
    } catch (err) {
        error.set(err.message);
        console.error('Error adding todo:', err);
    }
}

// Update a todo
export async function updateTodo(id, updates) {
    try {
        const response = await axios.put(`${API_URL}/${id}`, updates);
        todos.update(t => t.map(todo => todo.id === id ? response.data : todo));
        return response.data;
    } catch (err) {
        error.set(err.message);
        console.error('Error updating todo:', err);
    }
}

// Delete a todo
export async function deleteTodo(id) {
    try {
        await axios.delete(`${API_URL}/${id}`);
        todos.update(t => t.filter(todo => todo.id !== id));
    } catch (err) {
        error.set(err.message);
        console.error('Error deleting todo:', err);
    }
}

// Toggle todo completion
export async function toggleTodo(id, completed) {
    return updateTodo(id, { completed: !completed });
}

<script>
  import { toggleTodo, deleteTodo } from '../stores/todos.js';

  export let todo;

  async function handleToggle() {
    await toggleTodo(todo.id, todo.completed);
  }

  async function handleDelete() {
    if (confirm('Are you sure you want to delete this todo?')) {
      await deleteTodo(todo.id);
    }
  }
</script>

<div class="todo-item" class:completed={todo.completed}>
  <input
    type="checkbox"
    checked={todo.completed}
    on:change={handleToggle}
    class="checkbox"
  />
  <div class="content">
    <h3 class="title">{todo.title}</h3>
    {#if todo.description}
      <p class="description">{todo.description}</p>
    {/if}
    <small class="date">{new Date(todo.created_at).toLocaleDateString()}</small>
  </div>
  <button on:click={handleDelete} class="delete-btn">Delete</button>
</div>

<style>
  .todo-item {
    display: flex;
    align-items: center;
    padding: 12px;
    border: 1px solid #ddd;
    border-radius: 4px;
    margin-bottom: 8px;
    background-color: #fff;
    gap: 12px;
  }

  .todo-item.completed {
    background-color: #f5f5f5;
    opacity: 0.7;
  }

  .checkbox {
    width: 20px;
    height: 20px;
    cursor: pointer;
    flex-shrink: 0;
  }

  .content {
    flex: 1;
  }

  .title {
    margin: 0;
    font-size: 16px;
    font-weight: 500;
  }

  .todo-item.completed .title {
    text-decoration: line-through;
    color: #999;
  }

  .description {
    margin: 4px 0 0 0;
    font-size: 14px;
    color: #666;
  }

  .date {
    display: block;
    margin-top: 4px;
    color: #999;
    font-size: 12px;
  }

  .delete-btn {
    padding: 6px 12px;
    background-color: #ff6b6b;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    flex-shrink: 0;
  }

  .delete-btn:hover {
    background-color: #ff5252;
  }
</style>

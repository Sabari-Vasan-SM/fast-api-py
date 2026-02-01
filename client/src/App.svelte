<script>
  import { onMount } from 'svelte';
  import { todos, loading, error, fetchTodos } from './stores/todos.js';
  import AddTodo from './components/AddTodo.svelte';
  import TodoItem from './components/TodoItem.svelte';

  let completedCount = 0;

  onMount(() => {
    fetchTodos();
  });

  $: completedCount = $todos.filter(t => t.completed).length;
</script>

<main>
  <div class="container">
    <header>
      <h1>📝 My Todo List</h1>
      <p class="subtitle">Stay organized and productive</p>
    </header>

    {#if $error}
      <div class="error-message">
        <p>Error: {$error}</p>
        <button on:click={fetchTodos}>Retry</button>
      </div>
    {/if}

    <AddTodo />

    <div class="stats">
      <p>Total Todos: <strong>{$todos.length}</strong></p>
      <p>Completed: <strong>{completedCount}</strong></p>
      <p>Pending: <strong>{$todos.length - completedCount}</strong></p>
    </div>

    {#if $loading}
      <div class="loading">Loading todos...</div>
    {:else if $todos.length === 0}
      <div class="empty-state">
        <p>No todos yet. Add one to get started! 🚀</p>
      </div>
    {:else}
      <div class="todos-list">
        {#each $todos as todo (todo.id)}
          <TodoItem {todo} />
        {/each}
      </div>
    {/if}
  </div>
</main>

<style>
  :global(body) {
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
      Ubuntu, Cantarell, 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
      sans-serif;
    background-color: #f5f5f5;
  }

  main {
    min-height: 100vh;
    padding: 20px;
  }

  .container {
    max-width: 600px;
    margin: 0 auto;
  }

  header {
    text-align: center;
    margin-bottom: 30px;
  }

  header h1 {
    margin: 0;
    font-size: 32px;
    color: #333;
  }

  .subtitle {
    margin: 8px 0 0 0;
    color: #666;
    font-size: 14px;
  }

  .error-message {
    background-color: #ffebee;
    border: 1px solid #ef5350;
    color: #c62828;
    padding: 16px;
    border-radius: 4px;
    margin-bottom: 20px;
  }

  .error-message p {
    margin: 0 0 12px 0;
  }

  .error-message button {
    padding: 6px 12px;
    background-color: #ef5350;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }

  .error-message button:hover {
    background-color: #e53935;
  }

  .loading {
    text-align: center;
    padding: 40px 20px;
    color: #666;
    font-size: 16px;
  }

  .empty-state {
    text-align: center;
    padding: 40px 20px;
    color: #999;
  }

  .stats {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-bottom: 20px;
  }

  .stats p {
    background-color: white;
    padding: 12px;
    border-radius: 4px;
    margin: 0;
    text-align: center;
    font-size: 14px;
  }

  .stats strong {
    display: block;
    font-size: 20px;
    color: #4CAF50;
    margin-top: 4px;
  }

  .todos-list {
    background-color: white;
    border-radius: 8px;
    padding: 12px;
  }
</style>

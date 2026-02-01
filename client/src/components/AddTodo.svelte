<script>
  import { addTodo } from '../stores/todos.js';

  let title = '';
  let description = '';

  async function handleSubmit() {
    if (title.trim()) {
      await addTodo(title, description);
      title = '';
      description = '';
    }
  }

  function handleKeydown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  }
</script>

<div class="add-todo">
  <h2>Add New Todo</h2>
  <form on:submit|preventDefault={handleSubmit}>
    <div class="form-group">
      <input
        type="text"
        placeholder="Todo title..."
        bind:value={title}
        required
        class="input"
      />
    </div>
    <div class="form-group">
      <textarea
        placeholder="Description (optional)..."
        bind:value={description}
        on:keydown={handleKeydown}
        class="textarea"
      ></textarea>
    </div>
    <button type="submit" class="submit-btn">Add Todo</button>
  </form>
</div>

<style>
  .add-todo {
    background-color: #f9f9f9;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 20px;
  }

  .add-todo h2 {
    margin: 0 0 16px 0;
    font-size: 20px;
  }

  form {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .form-group {
    display: flex;
    flex-direction: column;
  }

  .input,
  .textarea {
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 14px;
    font-family: inherit;
  }

  .input:focus,
  .textarea:focus {
    outline: none;
    border-color: #4CAF50;
    box-shadow: 0 0 5px rgba(76, 175, 80, 0.3);
  }

  .textarea {
    min-height: 80px;
    resize: vertical;
  }

  .submit-btn {
    padding: 10px 20px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    font-weight: 500;
  }

  .submit-btn:hover {
    background-color: #45a049;
  }

  .submit-btn:active {
    transform: scale(0.98);
  }
</style>

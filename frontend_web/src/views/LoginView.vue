<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const username = ref('')
const password = ref('')
const errorMessage = ref('')
const loading = ref(false)

const handleLogin = () => {
  errorMessage.value = ''
  loading.value = true
  
  // Simulated authentication
  setTimeout(() => {
    if (username.value === 'admin' && password.value === 'admin') {
      localStorage.setItem('comunisafe_admin_auth', 'true')
      router.push('/')
    } else {
      errorMessage.value = 'Credenciales inválidas. Intente admin / admin'
      loading.value = false
    }
  }, 600)
}
</script>

<template>
  <div class="login-view">
    <div class="login-card">
      <div class="brand">
        <h1>ComuniSafe</h1>
        <p>Panel de Administración</p>
      </div>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="username">Usuario</label>
          <input 
            type="text" 
            id="username" 
            v-model="username" 
            placeholder="admin" 
            required
            :disabled="loading"
          />
        </div>
        
        <div class="form-group">
          <label for="password">Contraseña</label>
          <input 
            type="password" 
            id="password" 
            v-model="password" 
            placeholder="••••••" 
            required
            :disabled="loading"
          />
        </div>

        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>

        <button type="submit" class="login-button" :disabled="loading">
          {{ loading ? 'Iniciando sesión...' : 'Ingresar' }}
        </button>
      </form>
    </div>
  </div>
</template>

<style scoped>
.login-view {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: var(--color-background);
  font-family: inherit;
}

.login-card {
  background-color: var(--color-surface);
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05);
  width: 100%;
  max-width: 400px;
  border: 1px solid var(--color-border);
}

.brand {
  text-align: center;
  margin-bottom: 30px;
}

.brand h1 {
  color: var(--color-primary);
  font-size: 24px;
  margin: 0 0 5px 0;
}

.brand p {
  color: var(--color-text-muted);
  font-size: 14px;
  margin: 0;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text);
}

.form-group input {
  padding: 12px;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
  background-color: var(--color-background);
  color: var(--color-text);
}

.form-group input:focus {
  border-color: var(--color-primary);
}

.error-message {
  color: var(--color-severity-critico);
  font-size: 13px;
  text-align: center;
  background-color: #fde8e8;
  padding: 8px;
  border-radius: 6px;
}

.login-button {
  background-color: var(--color-primary);
  color: #ffffff;
  border: none;
  border-radius: 8px;
  padding: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
  margin-top: 10px;
}

.login-button:hover:not(:disabled) {
  opacity: 0.9;
}

.login-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
</style>

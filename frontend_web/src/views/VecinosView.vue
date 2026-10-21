<script setup lang="ts">
import { ref, computed } from 'vue'
import { authorProfiles } from '../data/mockData'

const searchQuery = ref('')

const users = Object.values(authorProfiles).map(u => ({
  ...u,
  email: u.name.toLowerCase().replace(/\s+/g, '.') + '@comunisafe.com'
}))

const filteredUsers = computed(() => {
  const q = searchQuery.value.toLowerCase()
  return users.filter(user => 
    q === '' || 
    user.name.toLowerCase().includes(q) || 
    user.email.toLowerCase().includes(q)
  )
})
</script>

<template>
  <div class="users-view">
    <header class="page-header">
      <div class="header-content">
        <h1>Vecinos</h1>
        <p>Directorio de usuarios registrados y activos en la comunidad</p>
      </div>
    </header>

    <div class="filters-bar">
      <div class="search-group">
        <label for="fSearch">Buscar Vecino</label>
        <input 
          type="text" 
          id="fSearch" 
          v-model="searchQuery" 
          placeholder="Buscar por nombre o correo..." 
          class="search-input"
        />
      </div>
    </div>

    <div class="table-container">
      <table class="data-table">
        <caption class="sr-only">Listado de vecinos registrados en la comunidad</caption>
        <thead>
          <tr>
            <th>Nombre del Usuario</th>
            <th>Correo Electrónico</th>
            <th>ID del Perfil</th>
            <th>Miembro desde</th>
            <th>Total Reportes</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="filteredUsers.length === 0">
            <td colspan="5" class="empty-state">No se encontraron vecinos con ese criterio.</td>
          </tr>
          <tr v-for="user in filteredUsers" :key="user.id">
            <td class="font-medium">{{ user.name }}</td>
            <td>{{ user.email }}</td>
            <td class="text-muted">{{ user.id }}</td>
            <td>{{ user.since }}</td>
            <td>
              <span class="badge" :class="user.reportCount > 10 ? 'high' : 'normal'">
                {{ user.reportCount }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.users-view {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.header-content h1 {
  margin: 0 0 8px 0;
  color: var(--color-primary);
  font-size: 28px;
}

.header-content p {
  margin: 0;
  color: var(--color-text-muted);
}

.filters-bar {
  background-color: var(--color-surface);
  padding: 16px 24px;
  border-radius: 12px;
  border: 1px solid var(--color-border);
  box-shadow: 0 2px 8px rgba(0,0,0,0.02);
}

.search-group {
  display: flex;
  align-items: center;
  gap: 12px;
}

.search-group label {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-muted);
}

.search-input {
  flex: 1;
  max-width: 400px;
  padding: 8px 12px;
  border-radius: 6px;
  border: 1px solid var(--color-border);
  background-color: var(--color-background);
  color: var(--color-text);
  font-size: 14px;
  outline: none;
  font-family: inherit;
}

.search-input:focus {
  border-color: var(--color-primary);
}

.table-container {
  background-color: var(--color-surface);
  border-radius: 12px;
  border: 1px solid var(--color-border);
  box-shadow: 0 2px 8px rgba(0,0,0,0.02);
  overflow: hidden;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.data-table th {
  padding: 16px 24px;
  background-color: rgba(66, 97, 125, 0.03);
  color: var(--color-text-muted);
  font-size: 13px;
  font-weight: 600;
  text-transform: uppercase;
  border-bottom: 1px solid var(--color-border);
}

.data-table td {
  padding: 16px 24px;
  border-bottom: 1px solid var(--color-border);
  font-size: 14px;
  color: var(--color-text);
}

.data-table tbody tr {
  transition: background-color 0.2s;
}

.data-table tbody tr:hover {
  background-color: var(--color-background);
}

.data-table tbody tr:last-child td {
  border-bottom: none;
}

.empty-state {
  text-align: center;
  padding: 40px !important;
  color: var(--color-text-muted) !important;
}

.font-medium {
  font-weight: 500;
  color: var(--color-text);
}

.text-muted {
  color: var(--color-text-muted);
}

.badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
}

.badge.normal {
  background-color: #f4f7fb;
  color: var(--color-text-muted);
}

.badge.high {
  background-color: #e2f0ff;
  color: var(--color-primary);
}
</style>

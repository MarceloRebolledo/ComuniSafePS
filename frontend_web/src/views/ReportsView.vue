<script setup lang="ts">
import { ref, computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useReportsStore } from '../stores/reportsStore'
import ReportModal from '../components/reports/ReportModal.vue'

const store = useReportsStore()
const { reports } = storeToRefs(store)

// Filters State
const searchQuery = ref('')
const filterCategory = ref('')
const filterSeverity = ref('')
const filterStatus = ref('')

// Modal State
const isModalOpen = ref(false)
const selectedReportId = ref<string | null>(null)

const openModal = (id: string) => {
  selectedReportId.value = id
  isModalOpen.value = true
}

const closeModal = () => {
  isModalOpen.value = false
  setTimeout(() => { selectedReportId.value = null }, 200)
}

// Filtered Data
const filteredReports = computed(() => {
  return reports.value.filter(report => {
    const q = searchQuery.value.toLowerCase()
    const matchSearch = q === '' || report.title.toLowerCase().includes(q) || report.authorName.toLowerCase().includes(q)
    const matchCategory = filterCategory.value ? report.category === filterCategory.value : true
    const matchSeverity = filterSeverity.value ? report.severity === filterSeverity.value : true
    const matchStatus = filterStatus.value ? report.status === filterStatus.value : true
    return matchSearch && matchCategory && matchSeverity && matchStatus
  })
})

// Export Logic
const exportToJson = () => {
  const dataStr = JSON.stringify(filteredReports.value, null, 2)
  const blob = new Blob([dataStr], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = `reportes_comunisafe_${new Date().getTime()}.json`
  link.click()
  URL.revokeObjectURL(url)
}

const exportToCsv = () => {
  const headers = ['ID', 'Titulo', 'Categoria', 'Urgencia', 'Estado', 'Autor', 'Fecha']
  const rows = filteredReports.value.map(r => [
    r.id,
    `"${r.title.replace(/"/g, '""')}"`,
    r.category,
    r.severity,
    r.status,
    `"${r.authorName.replace(/"/g, '""')}"`,
    r.createdAt.split('T')[0]
  ])
  
  const csvContent = [headers.join(','), ...rows.map(e => e.join(','))].join('\n')
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = `reportes_comunisafe_${new Date().getTime()}.csv`
  link.click()
  URL.revokeObjectURL(url)
}
</script>

<template>
  <div class="reports-view">
    <header class="page-header">
      <div class="header-content">
        <h1>Gestión de Publicaciones</h1>
        <p>Administra, filtra y exporta los reportes de la comunidad</p>
      </div>
      <div class="export-actions">
        <button class="btn btn-secondary" @click="exportToJson">Exportar a JSON</button>
        <button class="btn btn-primary" @click="exportToCsv">Exportar a CSV</button>
      </div>
    </header>

    <div class="filters-bar">
      <div class="filter-group search-group">
        <label for="fSearch">Buscar</label>
        <input 
          type="text" 
          id="fSearch" 
          v-model="searchQuery" 
          placeholder="Buscar por título o autor..." 
          class="search-input"
        />
      </div>

      <div class="filter-group">
        <label for="fCategory">Categoría</label>
        <select id="fCategory" v-model="filterCategory">
          <option value="">Todas</option>
          <option value="Basura">Basura</option>
          <option value="Luminarias">Luminarias</option>
          <option value="Calles">Calles</option>
          <option value="Animales">Animales</option>
          <option value="Seguridad">Seguridad</option>
          <option value="Otros">Otros</option>
        </select>
      </div>

      <div class="filter-group">
        <label for="fSeverity">Urgencia</label>
        <select id="fSeverity" v-model="filterSeverity">
          <option value="">Todas</option>
          <option value="normal">Normal</option>
          <option value="urgente">Urgente</option>
          <option value="critico">Crítico</option>
        </select>
      </div>

      <div class="filter-group">
        <label for="fStatus">Estado</label>
        <select id="fStatus" v-model="filterStatus">
          <option value="">Todos</option>
          <option value="Pendiente">Pendiente</option>
          <option value="En Proceso">En Proceso</option>
          <option value="Resuelto">Resuelto</option>
        </select>
      </div>
    </div>

    <div class="table-container">
      <table class="data-table">
        <caption class="sr-only">Listado y gestión de reportes de incidentes comunitarios</caption>
        <thead>
          <tr>
            <th>Título</th>
            <th>Categoría</th>
            <th>Urgencia</th>
            <th>Estado</th>
            <th>Fecha</th>
            <th>Autor</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="filteredReports.length === 0">
            <td colspan="6" class="empty-state">No hay reportes que coincidan con los filtros.</td>
          </tr>
          <tr v-for="report in filteredReports" :key="report.id" @click="openModal(report.id)">
            <td class="font-medium">{{ report.title }}</td>
            <td>
              <span class="badge category">{{ report.category }}</span>
            </td>
            <td>
              <span class="badge severity" :class="report.severity">{{ report.severity }}</span>
            </td>
            <td>
              <span class="badge status" :class="{
                'pendiente': report.status === 'Pendiente',
                'proceso': report.status === 'En Proceso',
                'resuelto': report.status === 'Resuelto'
              }">{{ report.status }}</span>
            </td>
            <td class="text-muted">{{ report.createdAt.split('T')[0] }}</td>
            <td class="text-muted">{{ report.authorName }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <ReportModal 
      :is-open="isModalOpen" 
      :report-id="selectedReportId" 
      @close="closeModal" 
    />
  </div>
</template>

<style scoped>
.reports-view {
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

.export-actions {
  display: flex;
  gap: 12px;
}

.btn {
  padding: 10px 16px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: opacity 0.2s;
}

.btn:hover {
  opacity: 0.9;
}

.btn-primary {
  background-color: var(--color-primary);
  color: white;
}

.btn-secondary {
  background-color: var(--color-surface);
  color: var(--color-primary);
  border: 1px solid var(--color-border);
}

.filters-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  background-color: var(--color-surface);
  padding: 16px 24px;
  border-radius: 12px;
  border: 1px solid var(--color-border);
  box-shadow: 0 2px 8px rgba(0,0,0,0.02);
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 12px;
}

.search-group {
  flex: 1;
  min-width: 250px;
}

.search-input {
  flex: 1;
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

.filter-group label {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-muted);
}

.filter-group select {
  padding: 8px 12px;
  border-radius: 6px;
  border: 1px solid var(--color-border);
  background-color: var(--color-background);
  color: var(--color-text);
  font-size: 14px;
  outline: none;
  cursor: pointer;
  font-family: inherit;
}

.filter-group select:focus {
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
  cursor: pointer;
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
  color: var(--color-text-muted) !important;
}

.badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
}

.badge.category {
  background-color: var(--color-background);
  border: 1px solid var(--color-border);
}

.badge.normal {
  background-color: #e7f8ee;
  color: var(--color-severity-normal);
}

.badge.urgente {
  background-color: #fff1e2;
  color: var(--color-severity-urgente);
}

.badge.critico {
  background-color: #fde8e8;
  color: var(--color-severity-critico);
}

.badge.status.pendiente {
  background-color: #f4f7fb;
  color: var(--color-text-muted);
}

.badge.status.proceso {
  background-color: #e2f0ff;
  color: var(--color-category-calles);
}

.badge.status.resuelto {
  background-color: #e7f8ee;
  color: var(--color-severity-normal);
}
</style>

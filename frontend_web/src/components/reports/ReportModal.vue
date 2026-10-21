<script setup lang="ts">
import { ref, watch } from 'vue'
import { useReportsStore } from '../../stores/reportsStore'
import type { Report, Status } from '../../data/mockData'

const props = defineProps<{
  reportId: string | null
  isOpen: boolean
}>()

const emit = defineEmits<{
  (e: 'close'): void
}>()

const store = useReportsStore()
const report = ref<Report | null>(null)
const selectedStatus = ref<Status>('Pendiente')

watch(() => props.reportId, (newId) => {
  if (newId) {
    const found = store.getReportById(newId)
    if (found) {
      report.value = { ...found } // clone to avoid direct mutation without save
      selectedStatus.value = found.status
    }
  } else {
    report.value = null
  }
})

const handleClose = () => {
  emit('close')
}

const handleStatusChange = () => {
  if (report.value && selectedStatus.value !== report.value.status) {
    store.updateReportStatus(report.value.id, selectedStatus.value)
    report.value.status = selectedStatus.value
  }
}
</script>

<template>
  <div v-if="isOpen && report" class="modal-overlay" @click.self="handleClose">
    <div class="modal-container">
      <header class="modal-header">
        <h2>Detalle de la Publicación</h2>
        <button class="close-button" @click="handleClose">&times;</button>
      </header>

      <div class="modal-body">
        <div class="report-content">
          <h3>{{ report.title }}</h3>
          <p class="description">{{ report.description }}</p>

          <div class="meta-grid">
            <div class="meta-item">
              <span class="label">Autor:</span>
              <span class="value">{{ report.authorName }}</span>
            </div>
            <div class="meta-item">
              <span class="label">Ubicación:</span>
              <span class="value">{{ report.location }}</span>
            </div>
            <div class="meta-item">
              <span class="label">Categoría:</span>
              <span class="badge category">{{ report.category }}</span>
            </div>
            <div class="meta-item">
              <span class="label">Urgencia:</span>
              <span class="badge severity" :class="report.severity">{{ report.severity }}</span>
            </div>
            <div class="meta-item">
              <span class="label">Fecha:</span>
              <span class="value">{{ report.createdAt.split('T')[0] }}</span>
            </div>
          </div>

          <div class="image-gallery" v-if="report.images && report.images.length">
            <h4>Imágenes Adjuntas</h4>
            <div class="images-container">
              <img v-for="(img, idx) in report.images" :key="idx" :src="img" alt="Report image" />
            </div>
          </div>
        </div>

        <div class="management-section">
          <h3>Gestión del Reporte</h3>
          <div class="status-control">
            <label for="statusSelect">Cambiar Estado:</label>
            <select id="statusSelect" v-model="selectedStatus" @change="handleStatusChange">
              <option value="Pendiente">Pendiente</option>
              <option value="En Proceso">En Proceso</option>
              <option value="Resuelto">Resuelto</option>
            </select>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(17, 26, 35, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 100;
  backdrop-filter: blur(2px);
}

.modal-container {
  background-color: var(--color-surface);
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  animation: modal-fade-in 0.2s ease-out;
}

@keyframes modal-fade-in {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid var(--color-border);
}

.modal-header h2 {
  margin: 0;
  font-size: 1.25rem;
  color: var(--color-text);
}

.close-button {
  background: none;
  border: none;
  font-size: 24px;
  color: var(--color-text-muted);
  cursor: pointer;
  line-height: 1;
  padding: 0;
  transition: color 0.2s;
}

.close-button:hover {
  color: var(--color-text);
}

.modal-body {
  padding: 24px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.report-content h3 {
  margin: 0 0 12px 0;
  font-size: 1.15rem;
  color: var(--color-primary);
}

.description {
  color: var(--color-text);
  line-height: 1.5;
  margin-bottom: 20px;
}

.meta-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  background-color: var(--color-background);
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.meta-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.meta-item .label {
  font-size: 12px;
  color: var(--color-text-muted);
  text-transform: uppercase;
  font-weight: 600;
}

.meta-item .value {
  font-size: 14px;
  color: var(--color-text);
}

.badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  width: fit-content;
}

.badge.category {
  background-color: var(--color-border);
  color: var(--color-text);
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

.image-gallery h4 {
  margin: 0 0 12px 0;
  color: var(--color-text);
}

.images-container {
  display: flex;
  gap: 12px;
  overflow-x: auto;
  padding-bottom: 8px;
}

.images-container img {
  width: 120px;
  height: 120px;
  object-fit: cover;
  border-radius: 8px;
  border: 1px solid var(--color-border);
}

.management-section {
  border-top: 1px solid var(--color-border);
  padding-top: 24px;
}

.management-section h3 {
  margin: 0 0 16px 0;
  font-size: 1rem;
  color: var(--color-text);
}

.status-control {
  display: flex;
  align-items: center;
  gap: 16px;
  background-color: var(--color-background);
  padding: 16px;
  border-radius: 8px;
}

.status-control label {
  font-weight: 500;
  color: var(--color-text);
}

.status-control select {
  padding: 8px 16px;
  border-radius: 6px;
  border: 1px solid var(--color-border);
  background-color: var(--color-surface);
  color: var(--color-text);
  font-size: 14px;
  cursor: pointer;
  outline: none;
  font-family: inherit;
}

.status-control select:focus {
  border-color: var(--color-primary);
}
</style>

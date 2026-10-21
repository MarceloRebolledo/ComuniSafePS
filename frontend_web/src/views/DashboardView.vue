<script setup lang="ts">
import { computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useReportsStore } from '../stores/reportsStore'
import { Chart as ChartJS, ArcElement, Tooltip, Legend, Title, CategoryScale, LinearScale, BarElement } from 'chart.js'
import { Doughnut, Bar } from 'vue-chartjs'

ChartJS.register(ArcElement, Tooltip, Legend, Title, CategoryScale, LinearScale, BarElement)

const store = useReportsStore()
const { reports } = storeToRefs(store)

// Metrics calculation
const totalReports = computed(() => reports.value.length)
const resolvedReports = computed(() => reports.value.filter(r => r.status === 'Resuelto').length)
const totalUsers = computed(() => {
  const users = new Set(reports.value.map(r => r.authorId))
  return users.size
})

// Categories Chart Data
const categoriesData = computed(() => {
  const counts = {
    Basura: 0, Luminarias: 0, Calles: 0, Animales: 0, Seguridad: 0, Otros: 0
  }
  reports.value.forEach(r => {
    if (counts[r.category as keyof typeof counts] !== undefined) {
      counts[r.category as keyof typeof counts]++
    }
  })

  return {
    labels: ['Basura', 'Luminarias', 'Calles', 'Animales', 'Seguridad', 'Otros'],
    datasets: [
      {
        backgroundColor: ['#E46D62', '#E7A53A', '#5092D9', '#9B7ADB', '#EC8B4C', '#73849A'],
        data: [counts.Basura, counts.Luminarias, counts.Calles, counts.Animales, counts.Seguridad, counts.Otros]
      }
    ]
  }
})

// Severities Chart Data
const severitiesData = computed(() => {
  const counts = {
    normal: 0, urgente: 0, critico: 0
  }
  reports.value.forEach(r => {
    counts[r.severity]++
  })

  return {
    labels: ['Normal', 'Urgente', 'Crítico'],
    datasets: [
      {
        label: 'Cantidad',
        backgroundColor: ['#33A36B', '#E58B3C', '#D95050'],
        data: [counts.normal, counts.urgente, counts.critico],
        borderRadius: 6
      }
    ]
  }
})

const chartOptionsCategories = {
  responsive: true,
  maintainAspectRatio: false,
  cutout: '75%',
  animation: {
    animateScale: true,
    animateRotate: true
  },
  plugins: {
    legend: {
      position: 'bottom' as const
    }
  }
}

const chartOptionsSeverities = {
  responsive: true,
  maintainAspectRatio: false,
  animation: {
    duration: 1000,
    easing: 'easeOutQuart' as const
  },
  scales: {
    x: {
      grid: { display: false }
    },
    y: {
      grid: { display: false },
      beginAtZero: true
    }
  },
  plugins: {
    legend: { display: false }
  }
}
</script>

<template>
  <div class="dashboard-view">
    <header class="page-header">
      <h1>Dashboard de Monitoreo</h1>
      <p>Resumen general del estado de la comunidad</p>
    </header>

    <div class="metrics-grid">
      <div class="metric-card">
        <h3>Total Publicaciones</h3>
        <div class="value">{{ totalReports }}</div>
      </div>
      <div class="metric-card">
        <h3>Reportes Resueltos</h3>
        <div class="value">{{ resolvedReports }}</div>
      </div>
      <div class="metric-card">
        <h3>USUARIOS</h3>
        <div class="value">{{ totalUsers }}</div>
      </div>
    </div>

    <div class="charts-grid">
      <div class="chart-card">
        <h3>Publicaciones por Categoría</h3>
        <div class="chart-container">
          <Doughnut :data="categoriesData" :options="chartOptionsCategories" />
        </div>
      </div>
      <div class="chart-card">
        <h3>Nivel de Urgencia</h3>
        <div class="chart-container">
          <Bar :data="severitiesData" :options="chartOptionsSeverities" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard-view {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.page-header h1 {
  margin: 0 0 8px 0;
  color: var(--color-primary);
  font-size: 28px;
}

.page-header p {
  margin: 0;
  color: var(--color-text-muted);
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.metric-card {
  background-color: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.02);
}

.metric-card h3 {
  margin: 0 0 12px 0;
  font-size: 14px;
  color: var(--color-text-muted);
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.metric-card .value {
  font-size: 36px;
  font-weight: 700;
  color: var(--color-primary);
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.chart-card {
  background-color: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.02);
}

.chart-card h3 {
  margin: 0 0 20px 0;
  font-size: 16px;
  color: var(--color-text);
}

.chart-container {
  position: relative;
  height: 250px;
  width: 100%;
}
</style>

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { initialReports, type Report, type Status } from '../data/mockData'

export const useReportsStore = defineStore('reports', () => {
  const reports = ref<Report[]>([...initialReports])

  const getReportById = (id: string) => {
    return reports.value.find(r => r.id === id)
  }

  const updateReportStatus = (id: string, newStatus: Status) => {
    const report = getReportById(id)
    if (report) {
      report.status = newStatus
    }
  }

  return {
    reports,
    getReportById,
    updateReportStatus
  }
})

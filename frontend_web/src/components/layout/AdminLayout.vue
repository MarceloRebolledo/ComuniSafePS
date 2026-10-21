<script setup lang="ts">
import { RouterLink, RouterView, useRouter } from 'vue-router'

const router = useRouter()

const handleLogout = () => {
  localStorage.removeItem('comunisafe_admin_auth')
  router.push('/login')
}
</script>

<template>
  <div class="admin-layout">
    <aside class="sidebar">
      <div class="logo">
        <img src="../../assets/logo-comunisafe.png" alt="ComuniSafe Logo" class="brand-logo" />
        ComuniSafe
      </div>
      <nav class="nav-links">
        <RouterLink to="/" exact-active-class="router-link-active">Dashboard</RouterLink>
        <RouterLink to="/publicaciones">Publicaciones</RouterLink>
        <RouterLink to="/vecinos">Vecinos</RouterLink>
      </nav>
      <div class="spacer"></div>
      <div class="logout">
        <a href="#" @click.prevent="handleLogout">Cerrar Sesión</a>
      </div>
    </aside>
    <main class="main-content">
      <header class="navbar">
        <h2>Panel de Administrador</h2>
      </header>
      <div class="content-area">
        <RouterView />
      </div>
    </main>
  </div>
</template>

<style scoped>
.admin-layout {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  background-color: var(--color-background);
  font-family: inherit;
}

.sidebar {
  width: 260px;
  background-color: var(--color-surface);
  border-right: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  padding: 0 0 24px 0;
  box-shadow: 2px 0 8px rgba(0,0,0,0.02);
  z-index: 10;
}

.logo {
  height: 70px;
  padding: 0 24px;
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--color-primary);
  border-bottom: 1px solid var(--color-border);
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  gap: 12px;
  box-sizing: border-box;
}

.brand-logo {
  height: 32px;
  width: auto;
  object-fit: contain;
}

.nav-links {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 0 16px;
}

.nav-links a {
  text-decoration: none;
  color: var(--color-text-muted);
  padding: 12px 16px;
  border-radius: 8px;
  transition: all 0.2s ease;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 12px;
}

.nav-links a:hover {
  background-color: rgba(66, 97, 125, 0.05); /* primary with opacity */
  color: var(--color-primary);
}

.nav-links a.router-link-active {
  background-color: var(--color-primary);
  color: #ffffff;
  box-shadow: 0 4px 12px rgba(66, 97, 125, 0.2);
}

.spacer {
  flex: 1;
}

.logout {
  padding: 0 16px;
}

.logout a {
  text-decoration: none;
  color: var(--color-severity-critico);
  padding: 12px 16px;
  border-radius: 8px;
  display: block;
  font-weight: 500;
  transition: all 0.2s;
  background-color: #fde8e8;
  text-align: center;
}

.logout a:hover {
  background-color: var(--color-severity-critico);
  color: white;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.navbar {
  height: 70px;
  background-color: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
  display: flex;
  align-items: center;
  padding: 0 32px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.02);
  z-index: 5;
  box-sizing: border-box;
}

.navbar h2 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--color-text);
  opacity: 0.8;
}

.content-area {
  flex: 1;
  overflow-y: auto;
  padding: 32px;
}
</style>

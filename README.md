# ComuniSafePS

Sistema colaborativo y plataforma integral para la seguridad vecinal y gestión comunitaria de incidentes.

Repositorio: https://github.com/MarceloRebolledo/ComuniSafePS

## Stack Tecnológico
- **Backend**: Python 3.11, FastAPI, SQLAlchemy, SQLite, Pydantic, Pytest.
- **Frontend Web**: Vue 3, TypeScript, Vite, Pinia, Chart.js.
- **Frontend Mobile**: Flutter (Dart).
- **Calidad y Análisis Estático**: SonarQube Community Edition (Docker), SonarScanner CLI, Pytest-Cov.

---

## Reproducción del Análisis de Calidad con SonarQube

Para reproducir el análisis estático de código fuente realizado sobre el repositorio, siga los siguientes pasos:

### 1. Requisitos Previos
- [Docker Desktop](https://www.docker.com/) instalado y en ejecución.
- Python 3.11 instalado (para regenerar reportes de cobertura en el backend).

### 2. Despliegue de la Instancia de SonarQube
Inicie el contenedor de SonarQube en el puerto 9000:
```powershell
docker run -d --name sonarqube-comunisafe -p 9000:9000 -e SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true sonarqube:lts-community
```
Espere aproximadamente 1 minuto a que el servicio inicialice. Puede comprobar el estado en su navegador en `http://localhost:9000`.

### 3. Generación del Reporte de Cobertura (Backend)
Desde la carpeta raíz del proyecto, ejecute las pruebas generando el reporte XML:
```powershell
cd backend
py -3.11 -m pytest --cov=app --cov-report=xml:coverage.xml tests/
cd ..
```

*(Opcional: Si el análisis se ejecuta mediante un contenedor Docker, asegúrese de que `<source>` en `backend/coverage.xml` apunte a `/usr/src/backend/app`).*

### 4. Ejecución del Escáner (SonarScanner CLI)
El archivo `sonar-project.properties` ya se encuentra configurado en la raíz del proyecto. Ejecute el escáner utilizando la imagen oficial de SonarSource:
```powershell
docker run --rm -v "${PWD}:/usr/src" sonarsource/sonar-scanner-cli
```

### 5. Visualización de Resultados
Una vez finalizado el escaneo, acceda a la interfaz web para explorar los hallazgos y métricas:
- **URL**: `http://localhost:9000/dashboard?id=comunisafe`
- **Pestaña "Overall Code"**: Métricas consolidadas (Bugs, Code Smells, Coverage, Duplications).
- **Pestaña "Issues"**: Detalle individual de cada regla evaluada.

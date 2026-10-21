# ComuniSafe - Flutter Frontend

Este es el frontend de **ComuniSafe** migrado de React Native a **Flutter con Dart**. Conserva el diseño estético premium original, modo oscuro dinámico, filtros avanzados, mapas interactivos y el sistema de reputación por niveles.

---

## Estructura del Proyecto

* `lib/config/`: Esquema de colores, utilidades de formato, categorías y niveles de reputación.
* `lib/models/`: Modelos de datos (`Report`, `Comment`, `UserProfile`, `ActivityNotification`) y datos mock.
* `lib/providers/`: Proveedores de estado (`AppDataProvider` para lógica del feed/auth y `ThemeProvider` para temas).
* `lib/services/`: Integración con API Komoot Photon para geocodificación y sugerencias.
* `lib/widgets/`: Componentes reutilizables personalizados de UI.
* `lib/screens/`: Pantallas principales (Feed, Tendencias, Crear, Alertas, Perfil, Ajustes, Detalles y Mapas).
* `test/`: Pruebas de unidad y widget para asegurar la estabilidad del código.

---

## Cómo Ejecutar y Desplegar en Android Studio

### 1. Generar Carpetas de Plataformas Nativas
Como este código contiene la estructura pura de Dart, debes generar las carpetas nativas de Android e iOS en tu máquina ejecutando el siguiente comando desde la raíz de la carpeta `Front/`:

```bash
flutter create --org com.comunisafe .
```

### 2. Configuración de Mapas (OpenStreetMap)
¡Buenas noticias! Hemos migrado los componentes de mapas de Google Maps a **OpenStreetMap (mediante la librería `flutter_map` en Dart)**. 

Esto significa que **no necesitas registrar ninguna clave API de Google Maps ni configurar archivos nativos** en Android (`AndroidManifest.xml`) ni en iOS (`AppDelegate.swift`). El mapa funcionará inmediatamente y de manera 100% gratuita una vez ejecutes la aplicación en el simulador o dispositivo.

---

## Ejecutar Pruebas Automatizadas

Hemos configurado un conjunto de pruebas unitarias y de widgets para que verifiques que no hay errores lógicos en el código:

```bash
flutter test
```

Esto ejecutará:
1. Pruebas unitarias de cálculo de distancia (`calculateDistanceKm`) y formatos relativos de fecha.
2. Pruebas lógicas del `AppDataProvider` (likes, añadir comentarios, crear reportes, reputación, login/logout).
3. Pruebas básicas del renderizado de widgets.

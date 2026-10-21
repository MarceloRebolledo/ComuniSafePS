export type Severity = "normal" | "urgente" | "critico";
export type Category =
  | "Basura"
  | "Luminarias"
  | "Calles"
  | "Animales"
  | "Seguridad"
  | "Otros";

export type Status = "Pendiente" | "En Proceso" | "Resuelto";

export interface Coordinates {
  lat: number;
  lng: number;
}

export interface Report {
  id: string;
  title: string;
  description: string;
  category: Category;
  severity: Severity;
  location: string;
  image: string;
  images: string[];
  likes: number;
  comments: number;
  views: number;
  authorId: string;
  authorName: string;
  createdAt: string;
  coordinates?: Coordinates;
  isLiked?: boolean;
  status: Status;
}

export interface Comment {
  id: string;
  authorId: string;
  authorName: string;
  text: string;
  createdAt: string;
}

export interface AuthorProfile {
  id: string;
  name: string;
  since: string;
  reportCount: number;
}

export interface UserProfile {
  id: string;
  name: string;
  email: string;
  bio: string;
  location: string;
  since: string;
  notificationsEnabled: boolean;
}

export interface ActivityNotification {
  id: string;
  type: "like" | "comment" | "follow" | "verified";
  title: string;
  description: string;
  createdAt: string;
  read: boolean;
  group: "hoy" | "semana";
}

const minutesAgo = (value: number) =>
  new Date(Date.now() - value * 60 * 1000).toISOString();

const hoursAgo = (value: number) =>
  new Date(Date.now() - value * 60 * 60 * 1000).toISOString();

const daysAgo = (value: number) =>
  new Date(Date.now() - value * 24 * 60 * 60 * 1000).toISOString();

export const CATEGORIES: Category[] = [
  "Basura",
  "Luminarias",
  "Calles",
  "Animales",
  "Seguridad",
  "Otros",
];

export const defaultProfile: UserProfile = {
  id: "user-self",
  name: "María García",
  email: "maria.garcia@email.com",
  bio: "Vecina activa comprometida con mejorar nuestra comunidad en Temuco.",
  location: "Temuco, Chile",
  since: "Ene. 2024",
  notificationsEnabled: true,
};

export const authorProfiles: Record<string, AuthorProfile> = {
  "user-self": {
    id: "user-self",
    name: "María García",
    since: "Ene. 2024",
    reportCount: 12,
  },
  "author-carlos": {
    id: "author-carlos",
    name: "Carlos Rodríguez",
    since: "Abr. 2024",
    reportCount: 6,
  },
  "author-ana": {
    id: "author-ana",
    name: "Ana López",
    since: "Feb. 2025",
    reportCount: 3,
  },
  "author-pedro": {
    id: "author-pedro",
    name: "Pedro Martínez",
    since: "Nov. 2023",
    reportCount: 15,
  },
  "author-luis": {
    id: "author-luis",
    name: "Luis Hernández",
    since: "Mar. 2023",
    reportCount: 27,
  },
  "author-sofia": {
    id: "author-sofia",
    name: "Sofía Ramírez",
    since: "May. 2024",
    reportCount: 5,
  },
  "author-roberto": {
    id: "author-roberto",
    name: "Roberto Flores",
    since: "Mar. 2024",
    reportCount: 8,
  },
  "author-claudia": {
    id: "author-claudia",
    name: "Claudia Vargas",
    since: "Ago. 2023",
    reportCount: 20,
  },
  "author-jorge": {
    id: "author-jorge",
    name: "Jorge Sepúlveda",
    since: "Abr. 2025",
    reportCount: 1,
  },
  "author-marcela": {
    id: "author-marcela",
    name: "Marcela Fuentes",
    since: "Feb. 2024",
    reportCount: 9,
  },
};

export const initialReports: Report[] = [
  {
    id: "1",
    title: "Bache en Av. Alemania",
    description:
      "Hoyo grande en la avenida que complica el tránsito vehicular. Lleva más de dos semanas y representa un riesgo real para autos, motos y ciclistas.",
    category: "Calles",
    severity: "normal",
    location: "Av. Alemania 0290, Temuco",
    image:
      "https://images.unsplash.com/photo-1539034629914-0e70a1243587?auto=format&fit=crop&w=1080&q=80",
    images: [
      "https://images.unsplash.com/photo-1539034629914-0e70a1243587?auto=format&fit=crop&w=1080&q=80",
      "https://images.unsplash.com/photo-1588802576579-dda4e609d68c?auto=format&fit=crop&w=1080&q=80",
      "https://images.unsplash.com/photo-1717185691293-4ecd7072b847?auto=format&fit=crop&w=1080&q=80",
    ],
    likes: 24,
    comments: 7,
    views: 156,
    authorId: "user-self",
    authorName: "María García",
    createdAt: hoursAgo(2),
    coordinates: { lat: -38.731, lng: -72.598 },
    status: "Pendiente",
  },
  {
    id: "2",
    title: "Microbasural creciendo",
    description:
      "Acumulación de basura cerca de la plaza que ya afecta a todo el sector. Los vecinos llevamos semanas pidiendo limpieza en este punto.",
    category: "Basura",
    severity: "normal",
    location: "Plaza Aníbal Pinto, Temuco",
    image:
      "https://images.unsplash.com/photo-1762805544291-cb128cf5ec80?auto=format&fit=crop&w=1080&q=80",
    images: [
      "https://images.unsplash.com/photo-1762805544291-cb128cf5ec80?auto=format&fit=crop&w=1080&q=80",
      "https://images.unsplash.com/photo-1765153394420-64df1d397034?auto=format&fit=crop&w=1080&q=80",
    ],
    likes: 67,
    comments: 23,
    views: 512,
    authorId: "author-carlos",
    authorName: "Carlos Rodríguez",
    createdAt: hoursAgo(5),
    coordinates: { lat: -38.737, lng: -72.591 },
    status: "Pendiente",
  },
  {
    id: "3",
    title: "Luminaria apagada hace días",
    description:
      "Poste de luz sin funcionar hace más de una semana en esta esquina. De noche el sector queda muy oscuro y da miedo pasar.",
    category: "Luminarias",
    severity: "normal",
    location: "Calle Bulnes 340, Temuco",
    image:
      "https://images.unsplash.com/photo-1671533596950-0617b81ee9b5?auto=format&fit=crop&w=1080&q=80",
    images: [
      "https://images.unsplash.com/photo-1671533596950-0617b81ee9b5?auto=format&fit=crop&w=1080&q=80",
    ],
    likes: 31,
    comments: 12,
    views: 189,
    authorId: "author-ana",
    authorName: "Ana López",
    createdAt: daysAgo(1),
    coordinates: { lat: -38.742, lng: -72.596 },
    status: "Pendiente",
  },
  {
    id: "4",
    title: "Perrito abandonado",
    description:
      "Llevo varios días viendo este perrito en el sector. Está asustado, no parece tener dueño y necesita ayuda urgente.",
    category: "Animales",
    severity: "urgente",
    location: "Parque Municipal, Temuco",
    image:
      "https://images.unsplash.com/photo-1691221679153-168621acfb4d?auto=format&fit=crop&w=1080&q=80",
    images: [
      "https://images.unsplash.com/photo-1691221679153-168621acfb4d?auto=format&fit=crop&w=1080&q=80",
    ],
    likes: 45,
    comments: 15,
    views: 234,
    authorId: "author-pedro",
    authorName: "Pedro Martínez",
    createdAt: hoursAgo(3),
    coordinates: { lat: -38.734, lng: -72.582 },
    status: "Pendiente",
  },
  {
    id: "5",
    title: "Acera rota frente al colegio",
    description:
      "El pavimento está completamente roto frente a la entrada del colegio. Los niños terminan bajándose a la calle para pasar.",
    category: "Calles",
    severity: "urgente",
    location: "Av. Caupolicán 0185, Temuco",
    image:
      "https://images.unsplash.com/photo-1717185691293-4ecd7072b847?auto=format&fit=crop&w=1080&q=80",
    images: [
      "https://images.unsplash.com/photo-1717185691293-4ecd7072b847?auto=format&fit=crop&w=1080&q=80",
      "https://images.unsplash.com/photo-1588802576579-dda4e609d68c?auto=format&fit=crop&w=1080&q=80",
    ],
    likes: 54,
    comments: 18,
    views: 421,
    authorId: "author-luis",
    authorName: "Luis Hernández",
    createdAt: hoursAgo(6),
    coordinates: { lat: -38.745, lng: -72.588 },
    status: "Pendiente",
  },
  {
    id: "6",
    title: "Propuesta: mejorar el parque",
    description:
      "Vecinos del sector queremos renovar este espacio. Hay plantas secas, bancas rotas y la cancha necesita pintura.",
    category: "Otros",
    severity: "normal",
    location: "Parque Balmaceda, Temuco",
    image:
      "https://images.unsplash.com/photo-1709331251565-d237b00babe6?auto=format&fit=crop&w=1080&q=80",
    images: [
      "https://images.unsplash.com/photo-1709331251565-d237b00babe6?auto=format&fit=crop&w=1080&q=80",
    ],
    likes: 42,
    comments: 31,
    views: 387,
    authorId: "author-sofia",
    authorName: "Sofía Ramírez",
    createdAt: daysAgo(2),
    coordinates: { lat: -38.728, lng: -72.586 },
    status: "Pendiente",
  },
  {
    id: "7",
    title: "Humo y llamas visibles desde la calle",
    description:
      "Hace varios minutos veo humo negro y llamas saliendo del cerro. Parece un incendio que está avanzando rápido. Eviten la zona.",
    category: "Seguridad",
    severity: "critico",
    location: "Cerro Ñielol sector norte, Temuco",
    image:
      "https://images.unsplash.com/photo-1767416129512-2012f3156f5b?auto=format&fit=crop&w=1080&q=80",
    images: [
      "https://images.unsplash.com/photo-1767416129512-2012f3156f5b?auto=format&fit=crop&w=1080&q=80",
      "https://images.unsplash.com/photo-1763823331995-e41c1cf3f24d?auto=format&fit=crop&w=1080&q=80",
    ],
    likes: 89,
    comments: 34,
    views: 623,
    authorId: "author-roberto",
    authorName: "Roberto Flores",
    createdAt: minutesAgo(12),
    coordinates: { lat: -38.722, lng: -72.587 },
    status: "Pendiente",
  },
  {
    id: "8",
    title: "Robo con violencia en el sector",
    description:
      "Acabo de ver a dos personas robando a un vecino en la esquina. Huyeron hacia el norte por Av. Alemania. Manténganse atentos.",
    category: "Seguridad",
    severity: "critico",
    location: "Av. Alemania esq. Prat, Temuco",
    image:
      "https://images.unsplash.com/photo-1582032404227-6217f0c29159?auto=format&fit=crop&w=1080&q=80",
    images: [
      "https://images.unsplash.com/photo-1582032404227-6217f0c29159?auto=format&fit=crop&w=1080&q=80",
    ],
    likes: 112,
    comments: 47,
    views: 891,
    authorId: "author-claudia",
    authorName: "Claudia Vargas",
    createdAt: minutesAgo(35),
    coordinates: { lat: -38.733, lng: -72.598 },
    status: "Pendiente",
  },
  {
    id: "9",
    title: "Choque entre dos autos, hay heridos",
    description:
      "Accidente fuerte en Av. Caupolicán. Hay personas lesionadas dentro de los autos y el tránsito está cortado en ambos sentidos.",
    category: "Calles",
    severity: "urgente",
    location: "Av. Caupolicán 0200, Temuco",
    image:
      "https://images.unsplash.com/photo-1668024439925-43a02c59ff75?auto=format&fit=crop&w=1080&q=80",
    images: [
      "https://images.unsplash.com/photo-1668024439925-43a02c59ff75?auto=format&fit=crop&w=1080&q=80",
      "https://images.unsplash.com/photo-1758552218340-4e2ebd457f48?auto=format&fit=crop&w=1080&q=80",
    ],
    likes: 38,
    comments: 19,
    views: 445,
    authorId: "author-jorge",
    authorName: "Jorge Sepúlveda",
    createdAt: hoursAgo(1),
    coordinates: { lat: -38.745, lng: -72.588 },
    status: "Pendiente",
  },
  {
    id: "10",
    title: "Sin agua desde esta mañana",
    description:
      "En toda la Villa Alegre llevamos desde temprano sin agua. Hay adultos mayores y niños en casa. Si alguien tiene información, avise por favor.",
    category: "Otros",
    severity: "urgente",
    location: "Villa Alegre, Temuco",
    image:
      "https://images.unsplash.com/photo-1762185226125-ee636980e3f1?auto=format&fit=crop&w=1080&q=80",
    images: [
      "https://images.unsplash.com/photo-1762185226125-ee636980e3f1?auto=format&fit=crop&w=1080&q=80",
    ],
    likes: 73,
    comments: 28,
    views: 534,
    authorId: "author-marcela",
    authorName: "Marcela Fuentes",
    createdAt: hoursAgo(2),
    coordinates: { lat: -38.748, lng: -72.581 },
    status: "Pendiente",
  },
];

export const initialComments: Record<string, Comment[]> = {
  "1": [
    {
      id: "1-1",
      authorId: "commenter-carlos",
      authorName: "Carlos Ramírez",
      text: "Ya llevo una semana pasando por ahí con cuidado. Ojalá lo arreglen pronto.",
      createdAt: hoursAgo(1),
    },
    {
      id: "1-2",
      authorId: "commenter-ana",
      authorName: "Ana Martínez",
      text: "Pasé ayer y está peor. El bache ya es enorme.",
      createdAt: minutesAgo(30),
    },
  ],
  "2": [
    {
      id: "2-1",
      authorId: "commenter-maria",
      authorName: "María López",
      text: "Es urgente. Ya se ven ratones cerca de la plaza.",
      createdAt: hoursAgo(2),
    },
  ],
  "4": [
    {
      id: "4-1",
      authorId: "commenter-laura",
      authorName: "Laura Sánchez",
      text: "¿Alguien conoce un rescatista de animales que pueda ir hoy?",
      createdAt: hoursAgo(1),
    },
    {
      id: "4-2",
      authorId: "commenter-diego",
      authorName: "Diego Torres",
      text: "Si nadie lo rescata hoy, mañana voy yo.",
      createdAt: minutesAgo(45),
    },
  ],
  "7": [
    {
      id: "7-1",
      authorId: "commenter-francisca",
      authorName: "Francisca Mora",
      text: "Yo también lo veo desde mi casa. El humo es muy oscuro.",
      createdAt: minutesAgo(8),
    },
    {
      id: "7-2",
      authorId: "commenter-pablo",
      authorName: "Pablo Cisternas",
      text: "Ya llamé a bomberos. Dijeron que una unidad va en camino.",
      createdAt: minutesAgo(5),
    },
  ],
  "8": [
    {
      id: "8-1",
      authorId: "commenter-gonzalo",
      authorName: "Gonzalo Muñoz",
      text: "Yo los vi también. Eran dos personas con chaqueta oscura.",
      createdAt: minutesAgo(20),
    },
  ],
};

export const initialActivityNotifications: ActivityNotification[] = [
  {
    id: "activity-1",
    type: "like",
    title: "A Carlos Ramírez le gustó tu reporte",
    description: "Bache en Av. Alemania",
    createdAt: minutesAgo(5),
    read: false,
    group: "hoy",
  },
  {
    id: "activity-2",
    type: "comment",
    title: "Ana López comentó tu reporte",
    description: "“Pasé ayer y está peor. Hay que difundirlo más.”",
    createdAt: hoursAgo(1),
    read: false,
    group: "hoy",
  },
  {
    id: "activity-3",
    type: "follow",
    title: "Pedro Martínez comenzó a seguirte",
    description: "Tu perfil sigue ganando visibilidad en la comunidad.",
    createdAt: hoursAgo(2),
    read: false,
    group: "hoy",
  },
  {
    id: "activity-4",
    type: "verified",
    title: "3 vecinos marcaron un reporte tuyo como resuelto",
    description: "Luminaria apagada en Calle Bulnes",
    createdAt: daysAgo(1),
    read: true,
    group: "semana",
  },
];

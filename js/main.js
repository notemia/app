/* ═══════════════════════════════════════════════
   Notemia Main JS: i18n, animations, nav
   ═══════════════════════════════════════════════ */

// ── i18n translations ──
const T = {
  // Meta
  meta_title: {
    ru: "Notemia apps. Приложения для психологов и их клиентов",
    en: "Notemia apps. Apps for Psychologists and Their Clients"
  },

  // Nav
  nav_apps:       { ru: "Приложения",   en: "Apps" },
  nav_audience:   { ru: "Для кого",     en: "For Whom" },
  nav_principles: { ru: "Принципы",     en: "Principles" },
  nav_support:    { ru: "Поддержка",    en: "Support" },
  nav_privacy:    { ru: "Приватность",  en: "Privacy" },

  // Hero
  hero_badge:   { ru: "Приложения для iPhone, iPad и Mac", en: "Apps for iPhone, iPad and Mac" },
  hero_title_1: { ru: "Инструменты для",     en: "Tools for" },
  hero_title_2: { ru: "психологов и клиентов", en: "psychologists & clients" },
  hero_sub: {
    ru: "Навигатор по запросам клиентов, модальностям и книгам. Дневник мыслей: когнитивные искажения и рефрейминг. Эмоции через тело: чек-ин и практики регуляции. Отношения: стадии, кризисы, типы привязанности. Концепции, сценарии, развитие ключевых способностей, рекомендуемые книги для психоаналитиков.",
    en: "Navigator for client requests, modalities & books. Thought journal: cognitive distortions & reframing. Emotions through the body: check-in & regulation practices. Relationships: stages, crises, attachment types. Concepts, scenarios, developing core capabilities, recommended books for psychoanalysts."
  },
  hero_cta:      { ru: "Смотреть приложения", en: "View Apps" },
  hero_notemia_cta: { ru: "AI-ассистент для практики", en: "" },
  stat_apps:     { ru: "приложений",          en: "apps" },
  stat_books:    { ru: "книг и статей",       en: "books & articles" },
  // Apps section
  apps_title: { ru: "Приложения полезные в практике психолога", en: "Apps useful in psychologist practice" },
  apps_sub: {
    ru: "Навигатор по литературе и запросам клиентов (PsyMap). Работа с мыслями и искажениями (2Reframe), с эмоциями через тело (Feel It). Отношения по научным моделям (Couple Bridge). Концепции, сценарии, развитие ключевых способностей, рекомендуемые книги для психоаналитиков (Becoming Analyst).",
    en: "Literature & client-request navigator (PsyMap). Thought & distortion work (2Reframe), emotions through the body (Feel It). Relationships via evidence-based models (Couple Bridge). Concepts, scenarios, core capabilities, recommended books for psychoanalysts (Becoming Analyst)."
  },

  // PsyMap
  psymap_badge:   { ru: "Для специалистов", en: "For Professionals" },
  psymap_tagline: { ru: "Учебный навигатор для студентов и начинающих психологов", en: "Study navigator for students and beginning psychologists" },
  psymap_desc: {
    ru: "20 типичных запросов клиентов с навигатором: формулировки, подготовка к сессии, красные флаги, супервизия. 6 модальностей, 50+ брифов книг, научные статьи. Всё в одном месте от первого клиента до уверенной практики.",
    en: "20 typical client requests with navigator: formulations, session prep, red flags, supervision. 6 modalities, 50+ book briefs, scientific articles. Everything in one place from first client to confident practice."
  },
  psymap_f1: { ru: "20 запросов клиентов", en: "20 client requests" },
  psymap_f2: { ru: "6 модальностей",      en: "6 modalities" },
  psymap_f3: { ru: "50+ книг",            en: "50+ books" },
  psymap_f4: { ru: "Офлайн",              en: "Offline" },

  // Couple Bridge
  couple_badge:   { ru: "Для пар", en: "For Couples" },
  couple_tagline: { ru: "Научный гид по отношениям", en: "Science-based relationship guide" },
  couple_desc: {
    ru: "40+ лет исследований Готтмана, Джонсон, Перель и Фишер в одном приложении. 7 стадий отношений, 10 кризисов с доказательными стратегиями, паттерны привязанности, 8 измерений отношений. Понимайте динамику, проходите кризисы, растите вместе.",
    en: "40+ years of research by Gottman, Johnson, Perel & Fisher in one app. 7 relationship stages, 10 crises with evidence-based strategies, attachment patterns, 8 relationship dimensions. Understand dynamics, navigate crises, grow together."
  },
  couple_f1: { ru: "7 стадий отношений", en: "7 relationship stages" },
  couple_f2: { ru: "10 кризисов",        en: "10 crises" },
  couple_f3: { ru: "Привязанность",      en: "Attachment" },
  couple_f4: { ru: "50+ ресурсов",       en: "50+ resources" },

  // 2Reframe
  reframe_badge:   { ru: "Для клиентов", en: "For Clients" },
  reframe_tagline: { ru: "Превратите шум мыслей в ясность", en: "Turn mental noise into clarity" },
  reframe_desc: {
    ru: "Дневник когнитивной работы. Запишите мысль, исследуйте 14 когнитивных искажений (Бек, Бёрнс), проанализируйте доказательства «за» и «против», переосмыслите с помощью 8 структурированных упражнений. Идеален как домашнее задание в терапии.",
    en: "Cognitive journal. Write down a thought, explore 14 cognitive distortions (Beck, Burns), analyze evidence for and against, reframe with 8 structured exercises. Perfect as therapy homework."
  },
  reframe_f1: { ru: "14 искажений",  en: "14 distortions" },
  reframe_f2: { ru: "8 упражнений",  en: "8 exercises" },
  reframe_f3: { ru: "Дневник",       en: "Journal" },
  reframe_f4: { ru: "Статистика",    en: "Insights" },

  // Feel It
  feelit_badge:   { ru: "Для клиентов", en: "For Clients" },
  feelit_tagline: { ru: "Распознавание эмоций через тело", en: "Recognize emotions through the body" },
  feelit_desc: {
    ru: "Чек-ин за 60 секунд: отметьте ощущения на силуэте тела, ответьте на уточняющие вопросы получите гипотезы эмоций с объяснением. 8 микропрактик регуляции по 60–120 секунд. Автоматическая стабилизация при высокой интенсивности.",
    en: "60-second check-in: mark sensations on a body silhouette, answer clarifying questions get emotion hypotheses with explanation. 8 regulation micro-practices (60–120 sec). Automatic stabilization at high intensity."
  },
  feelit_f1: { ru: "14 эмоций",      en: "14 emotions" },
  feelit_f2: { ru: "8 практик",      en: "8 practices" },
  feelit_f3: { ru: "Силуэт тела",   en: "Body silhouette" },
  feelit_f4: { ru: "Стабилизация",   en: "Stabilization" },

  // Becoming Analyst
  analyst_badge:   { ru: "Для аналитиков", en: "For Analysts" },
  analyst_tagline: { ru: "Для начинающих психоаналитиков", en: "For beginning psychoanalysts" },
  analyst_desc: {
    ru: "Концепции, клинические сценарии, ключевые способности, рекомендуемые книги. Подготовка к сессии и рефлексия после. Дневник аналитика и отслеживание профессионального роста. Как хороший супервизор расширяет видение, помогает думать, возвращает к процессу.",
    en: "Concepts, clinical scenarios, core capabilities, recommended books. Session preparation and post-session reflection. Analyst journal and growth tracking. Like a good supervisor expands perspective, helps think, brings you back to the process."
  },
  analyst_f1: { ru: "Концепции",       en: "Concepts" },
  analyst_f2: { ru: "Сценарии",        en: "Scenarios" },
  analyst_f3: { ru: "До/после сессии", en: "Pre/post session" },
  analyst_f4: { ru: "Дневник",         en: "Journal" },

  cta_appstore: { ru: "App Store", en: "App Store" },

  // Audience
  audience_label: { ru: "Аудитория", en: "Audience" },
  audience_title: { ru: "Для кого это создано", en: "Who It's For" },

  aud_student_t: { ru: "Студенты психологии", en: "Psychology Students" },
  aud_student_d: {
    ru: "PsyMap и Becoming Analyst помогут сориентироваться в литературе, подготовиться к первым клиентам и супервизии",
    en: "PsyMap and Becoming Analyst help navigate literature, prepare for first clients and supervision"
  },
  aud_pract_t: { ru: "Практикующие психологи", en: "Practicing Psychologists" },
  aud_pract_d: {
    ru: "Рекомендуйте 2Reframe и Feel It клиентам как инструменты между сессиями. PsyMap ваш справочник на каждый день",
    en: "Recommend 2Reframe and Feel It to clients as between-session tools. PsyMap your everyday reference"
  },
  aud_analyst_t: { ru: "Аналитики и супервизоры", en: "Analysts & Supervisors" },
  aud_analyst_d: {
    ru: "Becoming Analyst среда для углубления рефлексии, развития ключевых способностей и подготовки к сессиям",
    en: "Becoming Analyst environment for deepening reflection, developing core capabilities and session preparation"
  },
  aud_client_t: { ru: "Клиенты и пары", en: "Clients & Couples" },
  aud_client_d: {
    ru: "2Reframe для работы с мыслями, Feel It для понимания эмоций, Couple Bridge для осмысления отношений",
    en: "2Reframe for thought work, Feel It for understanding emotions, Couple Bridge for relationship insight"
  },

  // Principles
  princ_label: { ru: "Принципы",                    en: "Principles" },
  princ_title: { ru: "Что объединяет все приложения", en: "What Unites All Apps" },

  princ_1_t: { ru: "Доказательная база",  en: "Evidence-Based" },
  princ_1_d: {
    ru: "Контент основан на рецензируемых исследованиях и работах ведущих учёных. Никакой псевдонауки, никаких пустых обещаний.",
    en: "Content based on peer-reviewed research and leading scientists' work. No pseudoscience, no empty promises."
  },
  princ_2_t: { ru: "Полная приватность",  en: "Complete Privacy" },
  princ_2_d: {
    ru: "Все данные хранятся только на устройстве. Без аккаунтов, без трекинга, без передачи третьим лицам. Ваши мысли только ваши.",
    en: "All data stored on device only. No accounts, no tracking, no third-party sharing. Your thoughts are yours alone."
  },
  princ_3_t: { ru: "Работает офлайн",     en: "Works Offline" },
  princ_3_d: {
    ru: "Весь контент встроен в приложения. Интернет не нужен работайте в самолёте, на даче, где угодно.",
    en: "All content bundled in the apps. No internet needed work on a plane, at the cottage, anywhere."
  },
  princ_4_t: { ru: "Не заменяет специалиста", en: "Not a Replacement" },
  princ_4_d: {
    ru: "Приложения инструменты для обучения и самопомощи, не замена терапии и супервизии. В случае кризиса всегда к специалисту.",
    en: "These are learning and self-help tools, not replacements for therapy and supervision. In crisis always see a professional."
  },

  // CTA
  cta_title:  { ru: "Начните с того, что ближе",  en: "Start With What's Closest" },
  cta_sub: {
    ru: "Выберите приложение, которое решает вашу задачу прямо сейчас.",
    en: "Choose the app that solves your need right now."
  },
  cta_action: { ru: "К приложениям", en: "Go to Apps" },

  // Disclaimer
  disclaimer_text: {
    ru: "Все приложения являются образовательными и справочными инструментами. Они не являются медицинскими изделиями и не предназначены для диагностики, лечения или принятия клинических решений. В ситуациях кризиса или риска обращайтесь к квалифицированному специалисту.",
    en: "All apps are educational and reference tools. They are not medical devices and are not intended for diagnosis, treatment, or clinical decision-making. In crisis or risk situations, contact a qualified professional."
  },

  // Footer
  footer_apps_h:    { ru: "Приложения", en: "Apps" },
  footer_links_h:   { ru: "Ссылки",     en: "Links" },
  footer_contact_h: { ru: "Контакт",    en: "Contact" },
  footer_desc:      { ru: "Приложения для психологов и их клиентов", en: "Apps for psychologists and their clients" },
  footer_copy:      { ru: "© 2026 Notemia apps. Все права защищены.", en: "© 2026 Notemia apps. All rights reserved." },

  // Support page
  support_title: { ru: "Поддержка Notemia apps", en: "Support Notemia apps" },
  support_sub:   { ru: "Мы всегда готовы помочь", en: "We're here to help" },
  support_email_t: { ru: "Написать нам", en: "Email Us" },
  support_email_d: { ru: "Мы ответим в течение 24 часов", en: "We'll respond within 24 hours" },
  support_email_btn: { ru: "Отправить письмо", en: "Send Email" },
  support_faq_t:   { ru: "Частые вопросы", en: "FAQ" },
  support_faq_d:   { ru: "Быстрые ответы на популярные вопросы", en: "Quick answers to common questions" },
  support_bug_t:   { ru: "Сообщить об ошибке", en: "Report a Bug" },
  support_bug_d:   { ru: "Укажите приложение, устройство и версию iOS/macOS", en: "Include the app name, device and iOS/macOS version" },
  support_bug_btn: { ru: "Сообщить", en: "Report" },

  faq_q1: { ru: "Приложения работают без интернета?", en: "Do the apps work offline?" },
  faq_a1: { ru: "Да. Весь контент встроен в каждое приложение. Интернет после скачивания не нужен.", en: "Yes. All content is bundled in each app. No internet required after download." },
  faq_q2: { ru: "Нужен ли аккаунт?", en: "Do I need an account?" },
  faq_a2: { ru: "Нет. Все данные хранятся только на вашем устройстве. Регистрация не требуется.", en: "No. All data is stored on your device only. No registration required." },
  faq_q3: { ru: "Это замена терапии?", en: "Is this a replacement for therapy?" },
  faq_a3: { ru: "Нет. Все приложения: образовательные инструменты. Они не заменяют терапию, супервизию или обращение к специалисту.", en: "No. All apps are educational tools. They do not replace therapy, supervision, or professional help." },
  faq_q4: { ru: "Как восстановить подписку?", en: "How do I restore my subscription?" },
  faq_a4: { ru: "Откройте Настройки → Подписка → Восстановить покупки. Используйте тот же Apple ID.", en: "Go to Settings → Subscription → Restore Purchases. Use the same Apple ID." },
  faq_q5: { ru: "Какие устройства поддерживаются?", en: "What devices are supported?" },
  faq_a5: { ru: "iPhone и iPad с iOS 17+. Некоторые приложения также доступны на macOS 14+.", en: "iPhone and iPad with iOS 17+. Some apps are also available on macOS 14+." },

  // Privacy page
  privacy_title: { ru: "Политика конфиденциальности Notemia apps", en: "Privacy Policy Notemia apps" },
  privacy_sub:   { ru: "Последнее обновление: февраль 2026", en: "Last updated: February 2026" },
  priv_intro: {
    ru: "Настоящая политика распространяется на все приложения Notemia apps: PsyMap, Couple Bridge, 2Reframe, Feel It и Becoming Analyst.",
    en: "This policy applies to all Notemia apps: PsyMap, Couple Bridge, 2Reframe, Feel It, and Becoming Analyst."
  },
  priv_1_t: { ru: "Ваши данные", en: "Your Data" },
  priv_1_d: {
    ru: "Все приложения Notemia apps хранят данные исключительно на вашем устройстве. Мы не собираем, не передаём и не продаём никакую персональную информацию. Регистрация не требуется. Трекинг отсутствует.",
    en: "All Notemia apps store data exclusively on your device. We do not collect, transmit, or sell any personal information. No registration required. No tracking."
  },
  priv_2_t: { ru: "Подписки", en: "Subscriptions" },
  priv_2_d: {
    ru: "При оформлении подписки оплата обрабатывается Apple через App Store. Мы не имеем доступа к вашим платёжным данным. Подробности в политике конфиденциальности Apple.",
    en: "Subscription payments are processed by Apple through the App Store. We do not have access to your payment information. See Apple's privacy policy for details."
  },
  priv_3_t: { ru: "Аналитика Apple", en: "Apple Analytics" },
  priv_3_d: {
    ru: "Приложения распространяются через App Store. Стандартные сервисы Apple (отчёты о сбоях, аналитика App Store) могут собирать анонимизированные технические данные согласно политике Apple.",
    en: "Apps are distributed through the App Store. Standard Apple services (crash reports, App Store analytics) may collect anonymized technical data as described in Apple's privacy policy."
  },
  priv_4_t: { ru: "Контакт", en: "Contact" },
  priv_4_d: {
    ru: "По вопросам конфиденциальности: helpyoutofeel@gmail.com",
    en: "Privacy questions: helpyoutofeel@gmail.com"
  }
};

// ── Language engine ──
const LANG_KEY = "notemia-lang";

function getStoredLang() {
  const stored = localStorage.getItem(LANG_KEY);
  if (stored === "ru" || stored === "en") return stored;
  const nav = navigator.language || "en";
  return nav.toLowerCase().startsWith("ru") ? "ru" : "en";
}

let currentLang = getStoredLang();

function setLang(lang) {
  if (lang !== "ru" && lang !== "en") return;
  currentLang = lang;
  localStorage.setItem(LANG_KEY, lang);
  document.documentElement.lang = lang;
  applyTranslations();
  updateLangButtons();
}

function applyTranslations() {
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.getAttribute("data-i18n");
    if (T[key] && T[key][currentLang]) {
      if (el.tagName === "TITLE" || el.tagName === "META") {
        if (el.tagName === "TITLE") el.textContent = T[key][currentLang];
      } else {
        el.innerHTML = T[key][currentLang];
      }
    }
  });
}

function updateLangButtons() {
  document.querySelectorAll(".lang-btn").forEach(btn => {
    btn.classList.toggle("active", btn.getAttribute("data-lang") === currentLang);
  });
}

// ── Scroll animations ──
function initAnimations() {
  const observer = new IntersectionObserver(
    entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.1, rootMargin: "0px 0px -40px 0px" }
  );

  document.querySelectorAll(".anim-in").forEach(el => observer.observe(el));
}

// ── Nav scroll effect ──
function initNavScroll() {
  const nav = document.getElementById("nav");
  if (!nav) return;
  let ticking = false;
  window.addEventListener("scroll", () => {
    if (!ticking) {
      requestAnimationFrame(() => {
        nav.classList.toggle("nav--scrolled", window.scrollY > 20);
        ticking = false;
      });
      ticking = true;
    }
  });
}

// ── Mobile menu ──
function initBurger() {
  const burger = document.getElementById("burger");
  const links = document.getElementById("navLinks");
  if (!burger || !links) return;

  burger.addEventListener("click", () => {
    links.classList.toggle("open");
  });

  links.querySelectorAll(".nav__link").forEach(link => {
    link.addEventListener("click", () => links.classList.remove("open"));
  });
}

// ── FAQ accordion ──
function initFAQ() {
  document.querySelectorAll(".faq-q").forEach(btn => {
    btn.addEventListener("click", () => {
      const item = btn.closest(".faq-item");
      const wasOpen = item.classList.contains("open");
      document.querySelectorAll(".faq-item.open").forEach(el => el.classList.remove("open"));
      if (!wasOpen) item.classList.add("open");
    });
  });
}

// ── Smooth scroll for anchor links ──
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener("click", e => {
      const target = document.querySelector(link.getAttribute("href"));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    });
  });
}

// ── Init ──
document.addEventListener("DOMContentLoaded", () => {
  setLang(currentLang);
  initAnimations();
  initNavScroll();
  initBurger();
  initFAQ();
  initSmoothScroll();

  document.querySelectorAll(".lang-btn").forEach(btn => {
    btn.addEventListener("click", () => setLang(btn.getAttribute("data-lang")));
  });
});

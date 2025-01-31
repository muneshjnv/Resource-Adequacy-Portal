import { MenuItem } from './menu.model';

export const MENU: MenuItem[] = [
  {
    id: 1,
    label: 'MENUITEMS.MENU.TEXT',
    isTitle: true
  },




  {
    id: 2,
    label: 'MENUITEMS.DASHBOARD.TEXT',
    icon: 'mdi mdi-speedometer',
    subItems: [
      {
        id: 3,
        label: 'MENUITEMS.DASHBOARD.LIST.ANALYTICS',
        link: '/',
        parentId: 2
      },
    ]
  },


  {
    id: 8,
    label: 'MENUITEMS.APPS.TEXT',
    icon: 'mdi mdi-view-grid-plus-outline',
    subItems: [
      {
        id: 13,
        label: 'MENUITEMS.APPS.LIST.INTRADAY',
        link: 'fileuploads/intraday',
        parentId: 8
      },
      {
        id: 9,
        label: 'MENUITEMS.APPS.LIST.DAYAHEAD',
        link: 'fileuploads/dayahead',
        parentId: 8
      },
      {
        id: 10,
        label: 'MENUITEMS.APPS.LIST.WEEKAHEAD',
        link: 'fileuploads/weekahead',
        parentId: 8
      },
      {
        id: 11,
        label: 'MENUITEMS.APPS.LIST.MONTHAHEAD',
        link: 'fileuploads/monthahead',
        parentId: 8
      },
      {
        id: 12,
        label: 'MENUITEMS.APPS.LIST.YEARAHEAD',
        link: 'fileuploads/yearahead',
        parentId: 8
      }
      
    ]
  },
  {
    id: 10000,
    label: 'MENUITEMS.VIEWUPLOADS.TEXT',
    icon: 'mdi mdi-account-circle-outline',
    subItems: [
      {
        id: 10008,
        label: 'MENUITEMS.VIEWUPLOADS.LIST.INTRADAY',
        parentId: 10000,
        link: 'viewuploads/intraday'
      },
      {
        id: 10001,
        label: 'MENUITEMS.VIEWUPLOADS.LIST.DAYAHEAD',
        parentId: 10000,
        link: 'viewuploads/dayahead'
      },
      {
        id: 10004,
        label: 'MENUITEMS.VIEWUPLOADS.LIST.WEEKAHEAD',
        parentId: 10000,
        link: 'viewuploads/weekahead'
      },
      {
        id: 10005,
        label: 'MENUITEMS.VIEWUPLOADS.LIST.MONTHAHEAD',
        parentId: 10000,
        link: 'viewuploads/monthahead'
      },
      {
        id: 10006,
        label: 'MENUITEMS.VIEWUPLOADS.LIST.YEARAHEAD',
        parentId: 10000,
        link: 'viewuploads/yearahead'
      }
    ]
  },





  // to be done in next phase
  // {
  //   id: 10002,
  //   label: 'MENUITEMS.TIMINGENTRY.TEXT',
  //   icon: 'mdi mdi-sticker-text-outline',
  //   subItems: [{
  //     id: 10003,
  //     label: 'MENUITEMS.TIMINGENTRY.LIST.PENDING',
  //     parentId: 10002, 
  //     link: 'timingentry/pending'
  //   },
  //   {
  //     id: 10006,
  //     label: 'MENUITEMS.TIMINGENTRY.LIST.PREVIOUSCODES',
  //     parentId: 10002, 
  //     link: 'timingentry/previouscodes'
  //   }]
  // },
  // {              
  //   id: 10004,
  //   label: 'MENUITEMS.REPORTS.TEXT',
  //   icon: 'mdi mdi-form-select',
  //   subItems: [{
  //     id: 10005,
  //     label: 'MENUITEMS.REPORTS.LIST.LINEFLOWS',
  //     parentId: 10004, 
  //     link: 'reports/lineflows'
  //   },
  //   {
  //     id: 10007,
  //     label: 'MENUITEMS.REPORTS.LIST.MDP',
  //     parentId: 10004, 
  //     link: 'reports/mdp'
  //   }]
  // },





  // {
  //   id: 54,
  //   label: 'MENUITEMS.PAGES.TEXT',
  //   isTitle: true
  // },
  // {
  //   id: 55,
  //   label: 'MENUITEMS.AUTHENTICATION.TEXT',
  //   icon: 'mdi mdi-account-circle-outline',
  //   subItems: [
  //     {
  //       id: 56,
  //       label: 'MENUITEMS.AUTHENTICATION.LIST.SIGNIN',
  //       parentId: 49,
  //       subItems: [
  //         {
  //           id: 57,
  //           label: 'MENUITEMS.AUTHENTICATION.LIST.BASIC',
  //           link: '/',
  //           parentId: 56
  //         },
  //         {
  //           id: 58,
  //           label: 'MENUITEMS.AUTHENTICATION.LIST.COVER',
  //           link: '/',
  //           parentId: 56
  //         },
  //       ]
  //     },
  //     {
  //       id: 59,
  //       label: 'MENUITEMS.AUTHENTICATION.LIST.SIGNUP',
  //       parentId: 49,
  //       subItems: [
  //         {
  //           id: 60,
  //           label: 'MENUITEMS.AUTHENTICATION.LIST.BASIC',
  //           link: '/',
  //           parentId: 59
  //         },
  //         {
  //           id: 61,
  //           label: 'MENUITEMS.AUTHENTICATION.LIST.COVER',
  //           link: '/',
  //           parentId: 59
  //         },
  //       ]
  //     },
  //     {
  //       id: 62,
  //       label: 'MENUITEMS.AUTHENTICATION.LIST.PASSWORDRESET',
  //       parentId: 49,
  //       subItems: [
  //         {
  //           id: 63,
  //           label: 'MENUITEMS.AUTHENTICATION.LIST.BASIC',
  //           link: '/',
  //           parentId: 62
  //         },
  //         {
  //           id: 64,
  //           label: 'MENUITEMS.AUTHENTICATION.LIST.COVER',
  //           link: '/',
  //           parentId: 62
  //         },
  //       ]
  //     },
  //     {
  //       id: 62,
  //       label: 'MENUITEMS.AUTHENTICATION.LIST.PASSWORDCREATE',
  //       parentId: 49,
  //       subItems: [
  //         {
  //           id: 63,
  //           label: 'MENUITEMS.AUTHENTICATION.LIST.BASIC',
  //           link: '/',
  //           parentId: 62
  //         },
  //         {
  //           id: 64,
  //           label: 'MENUITEMS.AUTHENTICATION.LIST.COVER',
  //           link: '/',
  //           parentId: 62
  //         },
  //       ]
  //     },
  //     {
  //       id: 65,
  //       label: 'MENUITEMS.AUTHENTICATION.LIST.LOCKSCREEN',
  //       parentId: 49,
  //       subItems: [
  //         {
  //           id: 66,
  //           label: 'MENUITEMS.AUTHENTICATION.LIST.BASIC',
  //           link: '/',
  //           parentId: 65
  //         },
  //         {
  //           id: 67,
  //           label: 'MENUITEMS.AUTHENTICATION.LIST.COVER',
  //           link: '/',
  //           parentId: 65
  //         },
  //       ]
  //     },
  //     {
  //       id: 68,
  //       label: 'MENUITEMS.AUTHENTICATION.LIST.LOGOUT',
  //       parentId: 49,
  //       subItems: [
  //         {
  //           id: 69,
  //           label: 'MENUITEMS.AUTHENTICATION.LIST.BASIC',
  //           link: '/',
  //           parentId: 68
  //         },
  //         {
  //           id: 70,
  //           label: 'MENUITEMS.AUTHENTICATION.LIST.COVER',
  //           link: '/',
  //           parentId: 68
  //         },
  //       ]
  //     },
  //     {
  //       id: 71,
  //       label: 'MENUITEMS.AUTHENTICATION.LIST.SUCCESSMESSAGE',
  //       parentId: 49,
  //       subItems: [
  //         {
  //           id: 72,
  //           label: 'MENUITEMS.AUTHENTICATION.LIST.BASIC',
  //           link: '/',
  //           parentId: 71
  //         },
  //         {
  //           id: 73,
  //           label: 'MENUITEMS.AUTHENTICATION.LIST.COVER',
  //           link: '/',
  //           parentId: 71
  //         },
  //       ]
  //     },
  //     {
  //       id: 74,
  //       label: 'MENUITEMS.AUTHENTICATION.LIST.TWOSTEPVERIFICATION',
  //       parentId: 49,
  //       subItems: [
  //         {
  //           id: 75,
  //           label: 'MENUITEMS.AUTHENTICATION.LIST.BASIC',
  //           link: '/',
  //           parentId: 74
  //         },
  //         {
  //           id: 76,
  //           label: 'MENUITEMS.AUTHENTICATION.LIST.COVER',
  //           link: '/',
  //           parentId: 74
  //         },
  //       ]
  //     },
  //     {
  //       id: 77,
  //       label: 'MENUITEMS.AUTHENTICATION.LIST.ERRORS',
  //       parentId: 49,
  //       subItems: [
  //         {
  //           id: 78,
  //           label: 'MENUITEMS.AUTHENTICATION.LIST.404BASIC',
  //           link: '/',
  //           parentId: 77
  //         },
  //         {
  //           id: 79,
  //           label: 'MENUITEMS.AUTHENTICATION.LIST.404COVER',
  //           link: '/',
  //           parentId: 77
  //         },
  //         {
  //           id: 80,
  //           label: 'MENUITEMS.AUTHENTICATION.LIST.404ALT',
  //           link: '/',
  //           parentId: 77
  //         },
  //         {
  //           id: 81,
  //           label: 'MENUITEMS.AUTHENTICATION.LIST.500',
  //           link: '/',
  //           parentId: 77
  //         },
  //         {
  //           id: 81,
  //           label: 'MENUITEMS.AUTHENTICATION.LIST.OFFLINE',
  //           link: '/',
  //           parentId: 77
  //         },
  //       ]
  //     },
  //   ]
  // },
  // {
  //   id: 82,
  //   label: 'MENUITEMS.PAGES.TEXT',
  //   icon: 'mdi mdi-sticker-text-outline',
  //   subItems: [
  //     {
  //       id: 83,
  //       label: 'MENUITEMS.PAGES.LIST.STARTER',
  //       link: '/',
  //       parentId: 82
  //     },
  //     {
  //       id: 84,
  //       label: 'MENUITEMS.PAGES.LIST.PROFILE',
  //       parentId: 82,
  //       subItems: [
  //         {
  //           id: 85,
  //           label: 'MENUITEMS.PAGES.LIST.SIMPLEPAGE',
  //           link: '/',
  //           parentId: 84
  //         },
  //         {
  //           id: 86,
  //           label: 'MENUITEMS.PAGES.LIST.SETTINGS',
  //           link: '/',
  //           parentId: 84
  //         },
  //       ]
  //     },
  //     {
  //       id: 87,
  //       label: 'MENUITEMS.PAGES.LIST.TEAM',
  //       link: '/',
  //       parentId: 82
  //     },
  //     {
  //       id: 88,
  //       label: 'MENUITEMS.PAGES.LIST.TIMELINE',
  //       link: '/',
  //       parentId: 82
  //     },
  //     {
  //       id: 89,
  //       label: 'MENUITEMS.PAGES.LIST.FAQS',
  //       link: '/',
  //       parentId: 82
  //     },
  //     {
  //       id: 90,
  //       label: 'MENUITEMS.PAGES.LIST.PRICING',
  //       link: '/',
  //       parentId: 82
  //     },
  //     {
  //       id: 91,
  //       label: 'MENUITEMS.PAGES.LIST.GALLERY',
  //       link: '/',
  //       parentId: 82
  //     },
  //     {
  //       id: 92,
  //       label: 'MENUITEMS.PAGES.LIST.MAINTENANCE',
  //       link: '/',
  //       parentId: 82
  //     },
  //     {
  //       id: 93,
  //       label: 'MENUITEMS.PAGES.LIST.COMINGSOON',
  //       link: '/',
  //       parentId: 82
  //     },
  //     {
  //       id: 94,
  //       label: 'MENUITEMS.PAGES.LIST.SITEMAP',
  //       link: '/',
  //       parentId: 82
  //     },
  //     {
  //       id: 95,
  //       label: 'MENUITEMS.PAGES.LIST.SEARCHRESULTS',
  //       link: '/',
  //       parentId: 82
  //     },
  //     {
  //       id: 96,
  //       label: 'MENUITEMS.PAGES.LIST.PRIVACYPOLICY',
  //       link: '/',
  //       parentId: 82
  //     },
  //     {
  //       id: 97,
  //       label: 'MENUITEMS.PAGES.LIST.TERMS&CONDITIONS',
  //       link: '/',
  //       parentId: 82
  //     }
  //   ]
  // },
  // {
  //   id: 131,
  //   label: 'MENUITEMS.LANDING.TEXT',
  //   icon: 'ri-rocket-line',
  //   subItems: [
  //     {
  //       id: 85,
  //       label: 'MENUITEMS.LANDING.LIST.ONEPAGE',
  //       link: '/',
  //       parentId: 84
  //     },
  //     {
  //       id: 86,
  //       label: 'MENUITEMS.LANDING.LIST.NFTLANDING',
  //       link: '/',
  //       parentId: 84,
  //     },
  //     {
  //       id: 87,
  //       label: 'MENUITEMS.LANDING.LIST.JOB',
  //       link: '/',
  //       parentId: 84,
  //     },
  //   ]
  // },
  // {
  //   id: 96,
  //   label: 'MENUITEMS.COMPONENTS.TEXT',
  //   isTitle: true
  // },
  // {
  //   id: 97,
  //   label: 'MENUITEMS.BASEUI.TEXT',
  //   icon: 'mdi mdi-cube-outline',
  //   subItems: [
  //     {
  //       id: 98,
  //       label: 'MENUITEMS.BASEUI.LIST.ALERTS',
  //       link: '/',
  //       parentId: 97
  //     },
  //     {
  //       id: 99,
  //       label: 'MENUITEMS.BASEUI.LIST.BADGES',
  //       link: '/',
  //       parentId: 97
  //     },
  //     {
  //       id: 100,
  //       label: 'MENUITEMS.BASEUI.LIST.BUTTONS',
  //       link: '/',
  //       parentId: 97
  //     },
  //     {
  //       id: 101,
  //       label: 'MENUITEMS.BASEUI.LIST.COLORS',
  //       link: '/',
  //       parentId: 97
  //     },
  //     {
  //       id: 102,
  //       label: 'MENUITEMS.BASEUI.LIST.CARDS',
  //       link: '/',
  //       parentId: 97
  //     },
  //     {
  //       id: 103,
  //       label: 'MENUITEMS.BASEUI.LIST.CAROUSEL',
  //       link: '/',
  //       parentId: 97
  //     },
  //     {
  //       id: 104,
  //       label: 'MENUITEMS.BASEUI.LIST.DROPDOWNS',
  //       link: '/',
  //       parentId: 97
  //     },
  //     {
  //       id: 105,
  //       label: 'MENUITEMS.BASEUI.LIST.GRID',
  //       link: '/',
  //       parentId: 97
  //     },
  //     {
  //       id: 106,
  //       label: 'MENUITEMS.BASEUI.LIST.IMAGES',
  //       link: '/',
  //       parentId: 97
  //     },
  //     {
  //       id: 107,
  //       label: 'MENUITEMS.BASEUI.LIST.TABS',
  //       link: '/',
  //       parentId: 97
  //     },
  //     {
  //       id: 108,
  //       label: 'MENUITEMS.BASEUI.LIST.ACCORDION&COLLAPSE',
  //       link: '/',
  //       parentId: 97
  //     },
  //     {
  //       id: 109,
  //       label: 'MENUITEMS.BASEUI.LIST.MODALS',
  //       link: '/',
  //       parentId: 97
  //     },
  //     {
  //       id: 111,
  //       label: 'MENUITEMS.BASEUI.LIST.PLACEHOLDERS',
  //       link: '/',
  //       parentId: 97
  //     },
  //     {
  //       id: 112,
  //       label: 'MENUITEMS.BASEUI.LIST.PROGRESS',
  //       link: '/',
  //       parentId: 97
  //     },
  //     {
  //       id: 113,
  //       label: 'MENUITEMS.BASEUI.LIST.NOTIFICATIONS',
  //       link: '/',
  //       parentId: 97
  //     },
  //     {
  //       id: 114,
  //       label: 'MENUITEMS.BASEUI.LIST.MEDIAOBJECT',
  //       link: '/',
  //       parentId: 97
  //     },
  //     {
  //       id: 115,
  //       label: 'MENUITEMS.BASEUI.LIST.EMBEDVIDEO',
  //       link: '/',
  //       parentId: 97
  //     },
  //     {
  //       id: 116,
  //       label: 'MENUITEMS.BASEUI.LIST.TYPOGRAPHY',
  //       link: '/',
  //       parentId: 97
  //     },
  //     {
  //       id: 117,
  //       label: 'MENUITEMS.BASEUI.LIST.LISTS',
  //       link: '/',
  //       parentId: 97
  //     },
  //     {
  //       id: 117_1,
  //       label: 'MENUITEMS.BASEUI.LIST.LINKS',
  //       link: '/',
  //       badge: {
  //         variant: 'bg-success',
  //         text: 'MENUITEMS.DASHBOARD.BADGE',
  //       },
  //       parentId: 97
  //     },
  //     {
  //       id: 118,
  //       label: 'MENUITEMS.BASEUI.LIST.GENERAL',
  //       link: '/',
  //       parentId: 97
  //     },
  //     {
  //       id: 119,
  //       label: 'MENUITEMS.BASEUI.LIST.RIBBONS',
  //       link: '/',
  //       parentId: 97
  //     },
  //     {
  //       id: 120,
  //       label: 'MENUITEMS.BASEUI.LIST.UTILITIES',
  //       link: '/',
  //       parentId: 97
  //     }
  //   ]
  // },
  // {
  //   id: 121,
  //   label: 'MENUITEMS.ADVANCEUI.TEXT',
  //   icon: 'mdi mdi-layers-triple-outline',
  //   subItems: [
  //     {
  //       id: 122,
  //       label: 'MENUITEMS.ADVANCEUI.LIST.SWEETALERTS',
  //       link: '/',
  //       parentId: 121
  //     },
  //     {
  //       id: 124,
  //       label: 'MENUITEMS.ADVANCEUI.LIST.SCROLLBAR',
  //       link: '/',
  //       parentId: 121
  //     },
  //     {
  //       id: 126,
  //       label: 'MENUITEMS.ADVANCEUI.LIST.TOUR',
  //       link: '/',
  //       parentId: 121
  //     },
  //     {
  //       id: 127,
  //       label: 'MENUITEMS.ADVANCEUI.LIST.SWIPERSLIDER',
  //       link: '/',
  //       parentId: 121
  //     },
  //     {
  //       id: 128,
  //       label: 'MENUITEMS.ADVANCEUI.LIST.RATTINGS',
  //       link: '/',
  //       parentId: 121
  //     },
  //     {
  //       id: 129,
  //       label: 'MENUITEMS.ADVANCEUI.LIST.HIGHLIGHT',
  //       link: '/',
  //       parentId: 121
  //     },
  //     {
  //       id: 130,
  //       label: 'MENUITEMS.ADVANCEUI.LIST.SCROLLSPY',
  //       link: '/',
  //       parentId: 121
  //     }
  //   ]
  // },
  // {
  //   id: 131,
  //   label: 'MENUITEMS.WIDGETS.TEXT',
  //   icon: 'mdi mdi-puzzle-outline',
  //   link: '/s'
  // },
  // {
  //   id: 132,
  //   label: 'MENUITEMS.FORMS.TEXT',
  //   icon: 'mdi mdi-form-select',
  //   subItems: [
  //     {
  //       id: 133,
  //       label: 'MENUITEMS.FORMS.LIST.BASICELEMENTS',
  //       link: '/',
  //       parentId: 132
  //     },
  //     {
  //       id: 134,
  //       label: 'MENUITEMS.FORMS.LIST.FORMSELECT',
  //       link: '/',
  //       parentId: 132
  //     },
  //     {
  //       id: 135,
  //       label: 'MENUITEMS.FORMS.LIST.CHECKBOXS&RADIOS',
  //       link: '/',
  //       parentId: 132
  //     },
  //     {
  //       id: 136,
  //       label: 'MENUITEMS.FORMS.LIST.PICKERS',
  //       link: '/',
  //       parentId: 132
  //     },
  //     {
  //       id: 137,
  //       label: 'MENUITEMS.FORMS.LIST.INPUTMASKS',
  //       link: '/',
  //       parentId: 132
  //     },
  //     {
  //       id: 138,
  //       label: 'MENUITEMS.FORMS.LIST.ADVANCED',
  //       link: '/',
  //       parentId: 132
  //     },
  //     {
  //       id: 139,
  //       label: 'MENUITEMS.FORMS.LIST.RANGESLIDER',
  //       link: '/',
  //       parentId: 132
  //     },
  //     {
  //       id: 140,
  //       label: 'MENUITEMS.FORMS.LIST.VALIDATION',
  //       link: '/',
  //       parentId: 132
  //     },
  //     {
  //       id: 141,
  //       label: 'MENUITEMS.FORMS.LIST.WIZARD',
  //       link: '/',
  //       parentId: 132
  //     },
  //     {
  //       id: 142,
  //       label: 'MENUITEMS.FORMS.LIST.EDITORS',
  //       link: '/',
  //       parentId: 132
  //     },
  //     {
  //       id: 143,
  //       label: 'MENUITEMS.FORMS.LIST.FILEUPLOADS',
  //       link: '/',
  //       parentId: 132
  //     },
  //     {
  //       id: 144,
  //       label: 'MENUITEMS.FORMS.LIST.FORMLAYOUTS',
  //       link: '/',
  //       parentId: 132
  //     }
  //   ]
  // },
  // {
  //   id: 145,
  //   label: 'MENUITEMS.TABLES.TEXT',
  //   icon: 'mdi mdi-grid-large',
  //   subItems: [
  //     {
  //       id: 146,
  //       label: 'MENUITEMS.TABLES.LIST.BASICTABLES',
  //       link: '/',
  //       parentId: 145
  //     },
  //     {
  //       id: 147,
  //       label: 'MENUITEMS.TABLES.LIST.GRIDJS',
  //       link: '/',
  //       parentId: 145
  //     },
  //     {
  //       id: 148,
  //       label: 'MENUITEMS.TABLES.LIST.LISTJS',
  //       link: '/',
  //       parentId: 145
  //     }
  //   ]
  // },
  // {
  //   id: 149,
  //   label: 'MENUITEMS.CHARTS.TEXT',
  //   icon: 'mdi mdi-chart-donut',
  //   subItems: [
  //     {
  //       id: 150,
  //       label: 'MENUITEMS.CHARTS.LIST.APEXCHARTS',
  //       parentId: 149,
  //       subItems: [
  //         {
  //           id: 151,
  //           label: 'MENUITEMS.CHARTS.LIST.LINE',
  //           link: '/',
  //           parentId: 150
  //         },
  //         {
  //           id: 152,
  //           label: 'MENUITEMS.CHARTS.LIST.AREA',
  //           link: '/',
  //           parentId: 150
  //         },
  //         {
  //           id: 153,
  //           label: 'MENUITEMS.CHARTS.LIST.COLUMN',
  //           link: '/',
  //           parentId: 150
  //         },
  //         {
  //           id: 154,
  //           label: 'MENUITEMS.CHARTS.LIST.BAR',
  //           link: '/',
  //           parentId: 150
  //         },
  //         {
  //           id: 155,
  //           label: 'MENUITEMS.CHARTS.LIST.MIXED',
  //           link: '/',
  //           parentId: 150
  //         },
  //         {
  //           id: 156,
  //           label: 'MENUITEMS.CHARTS.LIST.TIMELINE',
  //           link: '/',
  //           parentId: 150
  //         },
  //         {
  //           id: 166_1,
  //           label: 'MENUITEMS.CHARTS.LIST.RANGEAREA',
  //           link: '/',
  //           badge: {
  //             variant: 'bg-success',
  //             text: 'MENUITEMS.DASHBOARD.BADGE',
  //           },
  //           parentId: 150
  //         },
  //         {
  //           id: 166_2,
  //           label: 'MENUITEMS.CHARTS.LIST.FUNNEL',
  //           link: '/',
  //           badge: {
  //             variant: 'bg-success',
  //             text: 'MENUITEMS.DASHBOARD.BADGE',
  //           },
  //           parentId: 150
  //         },
  //         {
  //           id: 157,
  //           label: 'MENUITEMS.CHARTS.LIST.CANDLSTICK',
  //           link: '/',
  //           parentId: 150
  //         },
  //         {
  //           id: 158,
  //           label: 'MENUITEMS.CHARTS.LIST.BOXPLOT',
  //           link: '/',
  //           parentId: 150
  //         },
  //         {
  //           id: 159,
  //           label: 'MENUITEMS.CHARTS.LIST.BUBBLE',
  //           link: '/',
  //           parentId: 150
  //         },
  //         {
  //           id: 160,
  //           label: 'MENUITEMS.CHARTS.LIST.SCATTER',
  //           link: '/',
  //           parentId: 150
  //         },
  //         {
  //           id: 161,
  //           label: 'MENUITEMS.CHARTS.LIST.HEATMAP',
  //           link: '/',
  //           parentId: 150
  //         },
  //         {
  //           id: 162,
  //           label: 'MENUITEMS.CHARTS.LIST.TREEMAP',
  //           link: '/',
  //           parentId: 150
  //         },
  //         {
  //           id: 163,
  //           label: 'MENUITEMS.CHARTS.LIST.PIE',
  //           link: '/',
  //           parentId: 150
  //         },
  //         {
  //           id: 164,
  //           label: 'MENUITEMS.CHARTS.LIST.RADIALBAR',
  //           link: '/',
  //           parentId: 150
  //         },
  //         {
  //           id: 165,
  //           label: 'MENUITEMS.CHARTS.LIST.RADAR',
  //           link: '/',
  //           parentId: 150
  //         },
  //         {
  //           id: 166,
  //           label: 'MENUITEMS.CHARTS.LIST.POLARAREA',
  //           link: '/',
  //           parentId: 150
  //         },
         
  //       ]
  //     },
  //     {
  //       id: 167,
  //       label: 'MENUITEMS.CHARTS.LIST.CHARTJS',
  //       link: '/',
  //       parentId: 149
  //     },
  //     {
  //       id: 168,
  //       label: 'MENUITEMS.CHARTS.LIST.ECHARTS',
  //       link: '/',
  //       parentId: 149
  //     }
  //   ]
  // },
  // {
  //   id: 169,
  //   label: 'MENUITEMS.ICONS.TEXT',
  //   icon: 'mdi mdi-android-studio',
  //   subItems: [
  //     {
  //       id: 170,
  //       label: 'MENUITEMS.ICONS.LIST.REMIX',
  //       link: '/',
  //       parentId: 169
  //     },
  //     {
  //       id: 171,
  //       label: 'MENUITEMS.ICONS.LIST.BOXICONS',
  //       link: '/',
  //       parentId: 169
  //     },
  //     {
  //       id: 172,
  //       label: 'MENUITEMS.ICONS.LIST.MATERIALDESIGN',
  //       link: '/',
  //       parentId: 169
  //     },
  //     {
  //       id: 173,
  //       label: 'MENUITEMS.ICONS.LIST.LINEAWESOME',
  //       link: '/',
  //       parentId: 169
  //     },
  //     {
  //       id: 174,
  //       label: 'MENUITEMS.ICONS.LIST.FEATHER',
  //       link: '/',
  //       parentId: 169
  //     },
  //     {
  //       id: 174,
  //       label: 'MENUITEMS.ICONS.LIST.CRYPTOSVG',
  //       link: '/',
  //       parentId: 169,
  //     },
  //   ]
  // },
  // {
  //   id: 175,
  //   label: 'MENUITEMS.MAPS.TEXT',
  //   icon: 'mdi mdi-map-marker-outline',
  //   subItems: [
  //     {
  //       id: 176,
  //       label: 'MENUITEMS.MAPS.LIST.GOOGLE',
  //       link: '/',
  //       parentId: 175
  //     },
  //     {
  //       id: 178,
  //       label: 'MENUITEMS.MAPS.LIST.LEAFLET',
  //       link: '/',
  //       parentId: 175
  //     }
  //   ]
  // },
  // {
  //   id: 179,
  //   label: 'MENUITEMS.MULTILEVEL.TEXT',
  //   icon: 'mdi mdi-share-variant-outline',
  //   subItems: [
  //     {
  //       id: 180,
  //       label: 'MENUITEMS.MULTILEVEL.LIST.LEVEL1.1',
  //       parentId: 179
  //     },
  //     {
  //       id: 181,
  //       label: 'MENUITEMS.MULTILEVEL.LIST.LEVEL1.2',
  //       subItems: [
  //         {
  //           id: 182,
  //           label: 'MENUITEMS.MULTILEVEL.LIST.LEVEL1.LEVEL2.1',
  //           parentId: 181,
  //         },
  //         {
  //           id: 183,
  //           label: 'MENUITEMS.MULTILEVEL.LIST.LEVEL1.LEVEL2.2',
  //           parentId: 181,
  //         }
  //       ]
  //     },
  //   ]
  // }

];

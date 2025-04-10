import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

// Component pages
import { DashboardComponent } from "./dashboards/dashboard/dashboard.component";

const routes: Routes = [
    {
        path: "",
        component: DashboardComponent
    },
    {
      path: '', loadChildren: () => import('./dashboards/dashboards.module').then(m => m.DashboardsModule)
    },
    {
      path: 'fileuploads', loadChildren: () => import('./fileuploads/fileuploads.module').then(m => m.FileuploadsModule)
    },
    {
      path: 'viewuploads', loadChildren: () => import('./viewuploads/viewuploads.module').then(m => m.ViewFileuploadsModule)
    },
    {
      path: 'timingentry', loadChildren: () => import('./timingentry/timingentry.module').then(m => m.TimingEntryModule)
    },
    {
      path: 'reports', loadChildren: () => import('./reports/reports.module').then(m => m.ReportsModule)
    }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PagesRoutingModule { }

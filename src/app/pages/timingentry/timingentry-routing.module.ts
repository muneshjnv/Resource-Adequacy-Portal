import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

// Component pages

import { TimingentryPendingComponent } from './timingentry-pending/timingentry-pending.component';

const routes: Routes = [
  
  {
    path: "pending",
    component: TimingentryPendingComponent
  }
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})

export class TimingEntryRoutingModule { }

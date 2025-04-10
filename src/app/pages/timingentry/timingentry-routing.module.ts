import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

// Component pages

import { TimingentryPendingComponent } from './timingentry-pending/timingentry-pending.component';
import { ElementPreviousCodesComponent } from './element-previous-codes/element-previous-codes.component';

const routes: Routes = [
  
  {
    path: "pending",
    component: TimingentryPendingComponent
  },
  {
    path: "previouscodes",
    component: ElementPreviousCodesComponent
  }
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})

export class TimingEntryRoutingModule { }

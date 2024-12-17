import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ViewDayaheadComponent } from './view-dayahead/view-dayahead.component';
import { ViewWeekaheadComponent } from './view-weekahead/view-weekahead.component';
import { ViewMonthaheadComponent } from './view-monthahead/view-monthahead.component';
import { ViewYearaheadComponent } from './view-yearahead/view-yearahead.component';
import { ViewIntradayComponent } from './view-intraday/view-intraday.component';

// Component pages


const routes: Routes = [
  {
    path: "intraday",
    component: ViewIntradayComponent
  },
  {
    path: "dayahead",
    component: ViewDayaheadComponent
  },
  {
    path: "weekahead",
    component: ViewWeekaheadComponent
  },
  {
    path: "monthahead",
    component: ViewMonthaheadComponent
  },
  {
    path: "yearahead",
    component: ViewYearaheadComponent
  }
 
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ViewFileuploadsRoutingModule { }

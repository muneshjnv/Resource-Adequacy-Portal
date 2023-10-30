import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ViewDayaheadComponent } from './view-dayahead/view-dayahead.component';
import { ViewWeekaheadComponent } from './view-weekahead/view-weekahead.component';

// Component pages


const routes: Routes = [
  {
    path: "dayahead",
    component: ViewDayaheadComponent
  },
  {
    path: "weekahead",
    component: ViewWeekaheadComponent
  }
 
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ViewFileuploadsRoutingModule { }

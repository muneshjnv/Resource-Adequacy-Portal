import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ViewDayaheadComponent } from './view-dayahead/view-dayahead.component';

// Component pages


const routes: Routes = [
  {
    path: "dayahead",
    component: ViewDayaheadComponent
  },
 
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ViewFileuploadsRoutingModule { }

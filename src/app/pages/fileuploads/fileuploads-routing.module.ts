import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DayaheadComponent } from './dayahead/dayahead.component';

// Component pages


const routes: Routes = [
  {
    path: "dayahead",
    component: DayaheadComponent
  },
 
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class FileuploadsRoutingModule { }

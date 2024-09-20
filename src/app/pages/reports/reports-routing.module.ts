import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LineflowsComponent } from './lineflows/lineflows.component';

const routes: Routes = [
  { path: 'lineflows', component: LineflowsComponent }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ReportsRoutingModule { }

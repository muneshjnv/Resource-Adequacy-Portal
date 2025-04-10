import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LineflowsComponent } from './lineflows/lineflows.component';
import { MdpComponent } from './mdp/mdp.component';

const routes: Routes = [
  { path: 'lineflows', component: LineflowsComponent },
  { path: 'mdp', component: MdpComponent }

];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ReportsRoutingModule { }

import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ReportsRoutingModule } from './reports-routing.module';
import { LineflowsComponent } from './lineflows/lineflows.component';
import { SharedModule } from 'src/app/shared/shared.module';
import { FlatpickrModule } from 'angularx-flatpickr';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { NgApexchartsModule } from 'ng-apexcharts';
import { MdpComponent } from './mdp/mdp.component';
import { NgSelectModule } from '@ng-select/ng-select';


@NgModule({
  declarations: [
    LineflowsComponent,
    MdpComponent
  ],
  imports: [
    CommonModule,
    ReportsRoutingModule,
    SharedModule,
    FlatpickrModule.forRoot(),
    FormsModule,
    ReactiveFormsModule,
    NgApexchartsModule,
    NgSelectModule
  ]
})
export class ReportsModule { }

import { NgModule, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { NgbTooltipModule, NgbDropdownModule, NgbAccordionModule, NgbProgressbarModule, NgbNavModule, NgbPaginationModule, NgbCollapseModule } from '@ng-bootstrap/ng-bootstrap';

// Feather Icon
import { FeatherModule } from 'angular-feather';
import { allIcons } from 'angular-feather/icons';

// Calendar package
import { FullCalendarModule } from '@fullcalendar/angular';
// Flat Picker
import { FlatpickrModule } from 'angularx-flatpickr';
// Simplebar
import { SimplebarAngularModule } from 'simplebar-angular';
// Ck Editer
import { CKEditorModule } from '@ckeditor/ckeditor5-angular';
// Counter
// import { CountToModule } from 'angular-count-to';
// Apex Chart Package
import { NgApexchartsModule } from 'ng-apexcharts';
import { LeafletModule } from '@asymmetrik/ngx-leaflet';

// Emoji Picker
import { PickerModule } from '@ctrl/ngx-emoji-mart';

// Load Icon
import { defineElement } from 'lord-icon-element';
import lottie from 'lottie-web';

//  Drag and drop
import { DndModule } from 'ngx-drag-drop';

// Select Droup down
import { NgSelectModule } from '@ng-select/ng-select';

// NG2 Search Filter
// import { Ng2SearchPipeModule } from 'ng2-search-filter';

// drag and droup row table
import { DragDropModule } from '@angular/cdk/drag-drop';
import { MatTableModule } from '@angular/material/table';

import { DatePipe } from '@angular/common';
import { DayaheadComponent } from './dayahead/dayahead.component';
import { FileuploadsRoutingModule } from './fileuploads-routing.module';
import { SharedModule } from 'src/app/shared/shared.module';
import { WeekaheadComponent } from './weekahead/weekahead.component';
import { MonthaheadComponent } from './monthahead/monthahead.component';
import { YearaheadComponent } from './yearahead/yearahead.component';
import { IntradayComponent } from './intraday/intraday.component';

// // Component Pages
// import { AppsRoutingModule } from "./apps-routing.module";
// import { SharedModule } from '../../shared/shared.module';
// import { CalendarComponent } from './calendar/calendar.component';
// import { ChatComponent } from './chat/chat.component';
// import { MailboxComponent } from './mailbox/mailbox.component';
// import { WidgetsComponent } from './widgets/widgets.component';
// import { EmailBasicComponent } from './email/email-basic/email-basic.component';
// import { EmailEcommerceComponent } from './email/email-ecommerce/email-ecommerce.component';
// import { FileManagerComponent } from './file-manager/file-manager.component';
// import { TodoComponent } from './todo/todo.component';

// import { SortByPipe } from '../apps/sort-by.pipe';
// import { ApikeyComponent } from './apikey/apikey.component';

// // Mask
// import { NgxMaskDirective, NgxMaskPipe, provideNgxMask, IConfig } from 'ngx-mask';

// // Sorting page
// import { NgbdApikeySortableHeader } from './apikey/apikey-sortable.directive';

// // Swiper Slider
// import { NgxUsefulSwiperModule } from 'ngx-useful-swiper';

@NgModule({
  declarations: [
    DayaheadComponent,
    WeekaheadComponent,
    MonthaheadComponent,
    YearaheadComponent,
    IntradayComponent
    
  ],
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    NgbTooltipModule,
    NgbDropdownModule,
    NgbAccordionModule,
    NgbProgressbarModule,
    NgbNavModule,
    NgbPaginationModule,
    NgbCollapseModule,
    FeatherModule.pick(allIcons),
    FullCalendarModule,
    FlatpickrModule.forRoot(),
    SimplebarAngularModule,
    CKEditorModule,
    // CountToModule,
    NgApexchartsModule,
    FileuploadsRoutingModule,
    SharedModule,
    PickerModule,
    DndModule,
    NgSelectModule,
    DragDropModule,
    MatTableModule,
    // Ng2SearchPipeModule,
    // NgxMaskDirective, 
    // NgxMaskPipe,
    // NgxUsefulSwiperModule ,
    LeafletModule,

  ],
  providers: [
    // provideNgxMask(),
    DatePipe
  ],
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class FileuploadsModule {
  constructor() {
    defineElement(lottie.loadAnimation);
  }
}

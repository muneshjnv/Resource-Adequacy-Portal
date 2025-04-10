import { DatePipe } from '@angular/common';
import { Component, ElementRef, TemplateRef, ViewChild } from '@angular/core';
import { FormControl, UntypedFormBuilder, UntypedFormGroup, Validators } from '@angular/forms';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import * as jspreadsheet from "jspreadsheet-ce";
import { ToastService } from '../../../account/login/toast-service';
import { DayAheadForecastService } from 'src/app/core/services/day-ahead-forecast.service';
import { TokenStorageService } from 'src/app/core/services/token-storage.service';
import Swal from 'sweetalert2';
import * as XLSX from 'xlsx';


const today = new Date();



@Component({
  selector: 'app-dayahead',
  templateUrl: './dayahead.component.html',
  styleUrls: ['./dayahead.component.scss']
})


export class DayaheadComponent {

  excelData: { header: any[]; rows: any[] } | null = null;

  // bread crumb items
  breadCrumbItems!: Array<{}>;

  spreadsheetData: any = [[]];

  loadedData: boolean = false;
  
  // disabledDate: Date = new Date(today.getTime() + 24 * 60 * 60 * 1000);
 
// Subtract one day from current time                       
  // this.disabledDate.setDate(this.disabledDate.getDate() - 1);
  

  tooltipvalidationform!: UntypedFormGroup;

  formsubmit!: boolean;

  uploading: boolean = false;

  

  

  // calendar
  // calendarEvents!: any[];
  // editEvent: any;
  // formEditData!: UntypedFormGroup;
  validationform!: UntypedFormGroup;

  // newEventDate: any;
  // category!: any[];
  submitted = false;
  submit!: boolean;
  previewClicked: boolean = false;
  userData: any;


  state_id_dict: any = {'bh_state': 1, 'jh_state':2, 'gr_state': 3, 'wb_state': 4, 'dvc_state':5, 'si_state': 7}

  // Calendar click Event
  // formData!: UntypedFormGroup;
  @ViewChild('editmodalShow') editmodalShow!: TemplateRef<any>;
  @ViewChild('modalShow') modalShow !: TemplateRef<any>;
  @ViewChild("spreadsheet", {static: true}) spreadsheet !: ElementRef<any>;
  // worksheets: jspreadsheet.worksheetInstance[];

  constructor(private modalService: NgbModal, private formBuilder: UntypedFormBuilder,public toastService: ToastService, private TokenStorageService: TokenStorageService , private dayAheadForecast: DayAheadForecastService ,private datePipe: DatePipe) { }
  
  ngOnInit(): void {

    this.breadCrumbItems = [
      { label: 'File Uploads' },
      { label: 'Day Ahead Forecast', active: true }
    ];
    /**
     * BreadCrumb
     */
    this.userData = this.TokenStorageService.getUser();


    


   

    
    
    // });

    this.validationform = this.formBuilder.group({
      // firstName: ['', [Validators.required, Validators.pattern('[a-zA-Z0-9]+')]],
      // lastName: ['', [Validators.required, Validators.pattern('[a-zA-Z0-9]+')]],
      // userName: ['', [Validators.required, Validators.pattern('[a-zA-Z0-9]+')]],
      // city: ['', [Validators.required, Validators.pattern('[a-zA-Z0-9]+')]],
      state: ['', [Validators.required, Validators.pattern('[a-zA-Z0-9]+')]],
      // zip: ['', [Validators.required, Validators.pattern('[a-zA-Z0-9]+')]],
      disabledDate: [new Date(today.getTime() + 24 * 60 * 60 * 1000)],
      excelFile: [null]
    });


    if(this.userData['role'] == 'user'){

      // console.log("Rinnegan")

      // console.log(this.state_id_dict[this.userData['username']]);
    
      this.validationform.get('state')!.setValue(this.userData['state_id']);
      this.validationform.get('state')!.disable();
      this.validationform.get('disabledDate')!.disable()
    }

    Swal.fire({text:'Data is prefilled with zeros, Please upload the file preview the data and then Upload!',confirmButtonColor: 'rgb(3, 142, 220)',});


  }

  


  // Validation


  // this._fetchData();


  data = [
    [1, '00:00 - 00:15', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, '00:15 - 00:30', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [3, '00:30 - 00:45', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [4, '00:45 - 01:00', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [5, '01:00 - 01:15', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [6, '01:15 - 01:30', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [7, '01:30 - 01:45', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [8, '01:45 - 02:00', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [9, '02:00 - 02:15', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [10, '02:15 - 02:30', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [11, '02:30 - 02:45', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [12, '02:45 - 03:00', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [13, '03:00 - 03:15', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [14, '03:15 - 03:30', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [15, '03:30 - 03:45', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [16, '03:45 - 04:00', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [17, '04:00 - 04:15', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [18, '04:15 - 04:30', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [19, '04:30 - 04:45', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [20, '04:45 - 05:00', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [21, '05:00 - 05:15', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [22, '05:15 - 05:30', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [23, '05:30 - 05:45', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [24, '05:45 - 06:00', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [25, '06:00 - 06:15', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [26, '06:15 - 06:30', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [27, '06:30 - 06:45', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [28, '06:45 - 07:00', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [29, '07:00 - 07:15', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [30, '07:15 - 07:30', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [31, '07:30 - 07:45', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [32, '07:45 - 08:00', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [33, '08:00 - 08:15', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [34, '08:15 - 08:30', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [35, '08:30 - 08:45', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [36, '08:45 - 09:00', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [37, '09:00 - 09:15', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [38, '09:15 - 09:30', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [39, '09:30 - 09:45', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [40, '09:45 - 10:00', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [41, '10:00 - 10:15', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [42, '10:15 - 10:30', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [43, '10:30 - 10:45', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [44, '10:45 - 11:00', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [45, '11:00 - 11:15', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [46, '11:15 - 11:30', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [47, '11:30 - 11:45', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [48, '11:45 - 12:00', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [49, '12:00 - 12:15', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [50, '12:15 - 12:30', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [51, '12:30 - 12:45', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [52, '12:45 - 13:00', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [53, '13:00 - 13:15', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [54, '13:15 - 13:30', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [55, '13:30 - 13:45', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [56, '13:45 - 14:00', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [57, '14:00 - 14:15', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [58, '14:15 - 14:30', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [59, '14:30 - 14:45', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [60, '14:45 - 15:00', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [61, '15:00 - 15:15', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [62, '15:15 - 15:30', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [63, '15:30 - 15:45', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [64, '15:45 - 16:00', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [65, '16:00 - 16:15', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [66, '16:15 - 16:30', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [67, '16:30 - 16:45', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [68, '16:45 - 17:00', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [69, '17:00 - 17:15', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [70, '17:15 - 17:30', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [71, '17:30 - 17:45', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [72, '17:45 - 18:00', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [73, '18:00 - 18:15', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [74, '18:15 - 18:30', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [75, '18:30 - 18:45', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [76, '18:45 - 19:00', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [77, '19:00 - 19:15', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [78, '19:15 - 19:30', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [79, '19:30 - 19:45', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [80, '19:45 - 20:00', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [81, '20:00 - 20:15', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [82, '20:15 - 20:30', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [83, '20:30 - 20:45', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [84, '20:45 - 21:00', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [85, '21:00 - 21:15', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [86, '21:15 - 21:30', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [87, '21:30 - 21:45', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [88, '21:45 - 22:00', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [89, '22:00 - 22:15', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [90, '22:15 - 22:30', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [91, '22:30 - 22:45', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [92, '22:45 - 23:00', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [93, '23:00 - 23:15', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [94, '23:15 - 23:30', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [95, '23:30 - 23:45', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [96, '23:45 - 00:00', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
   
  
  
  
  
  ];
  
  tempData: any = [];
  
  
  validSubmit() {
    this.submit = true;
  }
  
  /**
   * Returns form
   */
   get form() {
    return this.validationform.controls;
  }
  
  
  ngAfterViewInit() {
      jspreadsheet(this.spreadsheet.nativeElement, {
      data: this.data,
      // freezeColumns: 2,
      footers: [[ ' ','Total MUs', '=ROUND(SUM(C1:C96)/4000,2)' , '=ROUND(SUM(D1:D96)/4000,2)' , '=ROUND(SUM(E1:E96)/4000,2)','=ROUND(SUM(F1:F96)/4000,2)' , '=ROUND(SUM(G1:G96)/4000,2)' , '=ROUND(SUM(H1:H96)/4000,2)','=ROUND(SUM(I1:I96)/4000,2)' , '=ROUND(SUM(J1:J96)/4000,2)' , '=ROUND(SUM(K1:K96)/4000,2)','=ROUND(SUM(L1:L96)/4000,2)' , '=ROUND(SUM(M1:M96)/4000,2)' , '=ROUND(SUM(N1:N96)/4000,2)','=ROUND(SUM(O1:O96)/4000,2)' , '=ROUND(SUM(P1:P96)/4000,2)' , '=ROUND(SUM(Q1:Q96)/4000,2)','=ROUND(SUM(R1:R96)/4000,2)' , '=ROUND(SUM(S1:S96)/4000,2)' , '=ROUND(SUM(T1:T96)/4000,2)', '=ROUND(SUM(U1:U96)/4000,2)','=ROUND(SUM(V1:V96)/4000,2)' , '=ROUND(SUM(W1:W96)/4000,2)' , '=ROUND(SUM(X1:X96)/4000,2)', '=ROUND(SUM(Y1:Y96)/4000,2)' ]],
  
      tableOverflow: true,
      tableWidth: '1200px',
      tableHeight: '400px',
      columns: [
        {
            type: 'numeric',
            title: 'Block',
            width: '50',
            readOnly: true
            
        },
        {
            type: 'text',
            title: 'Period',
            width: '150',
            readOnly: true
            
        },
        {
            type: 'numeric',
            title: 'MW',
            width:'150',
            decimal: '.',
            mask: '0.00'
        },
        {
          type: 'numeric',
          title: 'MW',
          width:'100',
          decimal: '.',
            mask: '0.00'
      },
      {
        type: 'numeric',
        title: 'MW',
        width:'100',
        decimal: '.',
        mask: '0.00'
    },
      {
        type: 'numeric',
        title: 'MW',
        width:'100',
        decimal: '.',
        mask: '0.00'
      },
      {
        type: 'numeric',
        title: 'MW',
        width:'100',
        decimal: '.',
        mask: '0.00'
      },
    {
      type: 'numeric',
      title: 'MW',
      width:'100',
      decimal: '.',
      mask: '0.00'
    },{
      type: 'numeric',
      title: 'MW',
      width:'180',
      decimal: '.',
      mask: '0.00'
    },{
      type: 'numeric',
      title: 'MW',
      width:'100',
      decimal: '.',
      mask: '0.00'
    },{
      type: 'numeric',
      title: 'MW',
      width:'225'
    },{
      type: 'numeric',
      title: 'MW',
      width:'225',
      decimal: '.',
      mask: '0.00'
    },{
      type: 'numeric',
      title: 'MW',
      width:'225',
      decimal: '.',
      mask: '0.00'
    },{
      type: 'numeric',
      title: 'MW',
      width:'100',
      decimal: '.',
      mask: '0.00'
    },{
      type: 'numeric',
      title: 'MW',
      width:'300',
      decimal: '.',
      mask: '0.00'
    },{
      type: 'numeric',
      title: 'MW',
      width:'175',
      decimal: '.',
      mask: '0.00'
    },{
      type: 'numeric',
      title: 'MW',
      width:'175',
      decimal: '.',
      mask: '0.00'
    },{
      type: 'numeric',
      title: 'MW',
      width:'300',
      decimal: '.',
      mask: '0.00'
    },{
      type: 'numeric',
      title: 'MW',
      width:'300',
      decimal: '.',
      mask: '0.00'
    },{
      type: 'numeric',
      title: 'MW',
      width:'300',
      decimal: '.',
      mask: '0.00'
    },
    {
      type: 'numeric',
      title: 'MVar',
      width:'300',
      decimal: '.',
      mask: '0.00'
      
    },
    {
      type: 'numeric',
      title: 'MW',
      width:'300',
      decimal: '.',
      mask: '0.00'
    },
    {
      type: 'numeric',
      title: 'MW',
      width:'300',
      decimal: '.',
      mask: '0.00'
    },
    {
      type: 'numeric',
      title: 'MW',
      width:'300',
      decimal: '.',
      mask: '0.00'
    },
    {
      type: 'numeric',
      title: 'MW',
      width:'300',
      decimal: '.',
      mask: '0.00'
    },
    ],
    nestedHeaders:[
      
        [
            {
                title: 'Time',
                colspan: 2, 
                
            },
            {
              title: 'Forecasted Generation/ Availability',
              colspan: 12, 
              
              
          },
          {
            title: 'Gap between Demand & Availability (G) = (A)-(F)  Surplus(-) / Deficit (+)',
            colspan: 1, 
            
            
        },
        {
          title: 'Proposed Procurement',
          colspan: 2, 
          
        },
        {
          title: 'Shortages after day ahead procurement from market (J) =(G)-(H+I)  Surplus(-) / Deficit (+)',
          colspan: 1, 
          
      },
      {
        title: 'Relief through planned restrictions/ rostering/ power cuts (K)',
        colspan: 1, 
        
      },
      {
        title: 'Additional Load shedding proposed (L) = (J)-(K) Surplus(-) / Deficit (+)',
        colspan: 1, 
        
      },
      {
        title: 'Reactive Power Forecast',
        colspan: 1, 
        
      },
      {
        title: 'Secondary UP Ancillary Reserve(SRAS UP)',
        colspan: 1, 
        
      },
      {
        title: 'Secondary DOWN Ancillary Reserve(SRAS DOWN)',
        colspan: 1, 
        
      },
      {
        title: 'Tertiary UP Ancillary Reserve(TRAS UP)',
        colspan: 1, 
        
      },
      {
        title: 'Tertiary DOWN Ancillary Reserve(TRAS DOWN)',
        colspan: 1, 
        
      },
  
        ],
        [
            {
                title: '',
                colspan: 2,
            },
            {
              title: 'Forecasted Demand (A)',
              colspan: 1,
          },
          
  
            {
              title: 'From its own sources (Excluding Renewable)',
              colspan: 4, 
              
          },
          {
            title: 'From Renewable Sources',
            colspan: 4, 
            
        },
        {
          title: 'From ISGS & Other LTA & MTOA',
          colspan: 1, 
          
        },
        {
          title: 'From Bilateral Transaction (Advance + FCFS)',
          colspan: 1, 
          
        },
        {
          title: 'Total Availability',
          colspan: 1, 
          
        }, 
        {
          title: '',
          colspan: 1, 
          
        },  
        {
          title: 'Under Bilateral Transaction (Day Ahead+ Contingency) (H)',
          colspan: 1, 
          
        },
        {
          title: 'Through Power Exchange (I)',
          colspan: 1, 
          
        },
        {
          title: '',
          colspan: 1, 
          
        },   {
          title: '',
          colspan: 1, 
          
        },   {
          title: '',
          colspan: 1, 
          
        },  
        {
          title: '',
          colspan: 1, 
          
        },  
        {
          title: '',
          colspan: 1, 
          
        },
        {
          title: '',
          colspan: 1, 
          
        },
        {
          title: '',
          colspan: 1, 
          
        },
        {
          title: '',
          colspan: 1, 
          
        },
        ],
        [
          {
              title: '',
              colspan: 2,
          },
          {
            title: '',
            colspan: 1,
        },
        
          {
            title: 'Thermal (Coal + Lignite)',
            colspan: 1, 
            
        },
        {
          title: 'Gas',
          colspan: 1, 
          
      },
        {
          title: 'Hydro',
          colspan: 1, 
          
      },
        {
          title: 'Total (B)',
          colspan: 1, 
          
      },
        {
        title: 'Solar',
        colspan: 1, 
        
        },
        {
          title: 'Wind',
          colspan: 1, 
          
        },
        {
          title: 'Other RES (biomass etc.)',
          colspan: 1, 
          
        },
        {
          title: 'Total (C)',
          colspan: 1, 
          
        },
        {
          title: '',
          colspan: 1, 
          
        },
        {
          title: '',
          colspan: 1, 
          
        },
        {
          title: '',
          colspan: 1, 
          
        },
        {
          title: '',
          colspan: 1, 
          
        },  
        {
          title: '',
          colspan: 1, 
          
        },
        {
          title: '',
          colspan: 1, 
          
        },
        {
          title: '',
          colspan: 1, 
          
        },   {
          title: '',
          colspan: 1, 
          
        },   {
          title: '',
          colspan: 1, 
          
        },    
  
        {
          title: '',
          colspan: 1, 
          
        },  
        {
          title: '',
          colspan: 1, 
          
        },  
        {
          title: '',
          colspan: 1, 
          
        },  
        {
          title: '',
          colspan: 1, 
          
        },  
        {
          title: '',
          colspan: 1, 
          
        },  
          
      ],
    ],
  
    updateTable(instance, cell, colIndex, rowIndex, value, displayedValue, cellName) {
  
      if(colIndex == 2 ) {
        const exactValue = value.toString()
        if(typeof value !== 'number' && Number.isNaN(Number.parseInt(exactValue))){
          cell.style.background = '#ffcccb'
          Swal.fire({text:'Your Data has some errors, They are highlighted. Please check and Update',confirmButtonColor: 'rgb(3, 142, 220)',});
          
        }
        
  
        const modifiedValue = value.toString()
      // console.log(modifiedValue)
      if(typeof modifiedValue === "number" || !Number.isNaN(Number.parseFloat(modifiedValue))) {
        // console.log("enter the dragon!")
        cell.style.background = 'white';
      }
      
      
        
        
      }
    },
  
   
  
    // onchange(element, cell, colIndex, rowIndex, newValue, oldValue) {
    //   // console.log('Rinnegan')
    //   // console.log(oldValue)
    //   // console.log(typeof newValue);
  
    //   // if(typeof newValue === 'number' ){
    //   //   cell.style.background = 'white';
    //   // }
  
    //   // console.log(Number.is(newValue));
    //   // const stringValue = cellValue.toString();
    //   const modifiedValue = newValue.toString()
    //   console.log(modifiedValue)
    //   console.log(typeof modifiedValue === "number" || !Number.isNaN(Number.parseFloat(modifiedValue)));
    //   if(typeof modifiedValue === "number" || !Number.isNaN(Number.parseFloat(modifiedValue))) {
    //     cell.style.background = 'blue';
    //   }
  
    // },
  
    
    
    
    
  
    
  
    
    
    });


        
  }
  
  formSubmit() {
    this.formsubmit = true;
  }
  
  
  confirm() {

    if(this.validationform.get('excelFile')!.value == null) {
      Swal.fire({text:'It seems you have not uploaded the file, Please upload the file!',confirmButtonColor: 'rgb(3, 142, 220)',});
  
    }
    else {

      // console.log("Entered Else part!")

      if(this.validationform.valid) {

        Swal.fire({
          title: 'Are you sure?',
          text: 'You won\'t be able to revert this!',
          icon: 'warning',
          showCancelButton: true,
          confirmButtonColor: 'rgb(3, 142, 220)',
          cancelButtonColor: 'rgb(243, 78, 78)',
          confirmButtonText: 'Yes, Insert it!'
        }).then(result => {
          if (result.value) {
            const formData = new FormData();
            formData.append('state', this.validationform.get('state')!.value);
            formData.append('disabledDate', this.validationform.get('disabledDate')!.value);
            formData.append('excelFile', this.validationform.get('excelFile')!.value);
            formData.append('data', JSON.stringify(this.spreadsheet.nativeElement.jexcel.getData()))

            this.uploading = true;
              
              this.dayAheadForecast.uploadDayAheadFile(formData).subscribe((res: any)=> {
                this.uploading = false;
                if('error' in res) {
                  // console.log(res['error'])
                }
                else {
                  // console.log(res["message"]);
                  // this.toastService.show(res['message'], { classname: 'bg-success text-white', delay: 5000 });
        
                  
                  Swal.fire({
                    text: res['message'],
                    icon: 'success',
                    confirmButtonColor: 'rgb(3, 142, 220)',
                    confirmButtonText: 'OK'
                  });

                  this.spreadsheet.nativeElement.jexcel.setData(this.data);
        
        
        
        
                }
          
              })
                  }
        });
    
    
    
    
      }

    }
   
    
  }
  
  
  onUpload() {
    // console.log(this.validationform.get('excelFile')!.value)
    if(this.validationform.get('excelFile')!.value == null) {
      Swal.fire({text:'It seems you have not uploaded the file, Please upload the file!',confirmButtonColor: 'rgb(3, 142, 220)',});
  
    }
    if(this.validationform.valid) {
  
  
  
      const formData = new FormData();
    formData.append('state', this.validationform.get('state')!.value);
    formData.append('disabledDate', this.validationform.get('disabledDate')!.value);
    formData.append('excelFile', this.validationform.get('excelFile')!.value);
    formData.append('data', JSON.stringify(this.spreadsheet.nativeElement.jexcel.getData()))
      
      this.dayAheadForecast.uploadDayAheadFile(formData).subscribe((res: any)=> {
        if('error' in res) {
          // console.log(res['error'])
        }
        else {
          // console.log(res["message"]);
          // this.toastService.show(res['message'], { classname: 'bg-success text-white', delay: 5000 });

          
          Swal.fire({
            text: res['message'],
            icon: 'success',
            confirmButtonColor: 'rgb(3, 142, 220)',
            confirmButtonText: 'OK'
          });




        }
  
      })
  
    }
  
  
  
    
  }
  
  
  get formData() {
    return this.tooltipvalidationform.controls;
  }
  
  
  previewButtonClicked() {
    this.previewClicked = true;
  }
  
  downloadExcel() {
    // Define the path to the Excel file in the assets folder
    const excelFilePath = 'assets/Day-Ahead Demand Forecast format (from States).xlsx';
  
    // Trigger the download by creating a temporary <a> element
    const a = document.createElement('a');
    a.href = excelFilePath;
    a.download = 'sample.xlsx'; // Specify the desired file name
  
    // Programmatically trigger a click event to initiate the download
    a.click();
  }
  
  
  handleFileInput(event: any) {

    // console.log(this.spreadsheet.nativeElement.jexcel);
    const file = event.target.files[0];
    this.validationform.get('excelFile')!.setValue(file);
    if (!file) return;
  
    const reader = new FileReader();
    reader.onload = (e: any) => {
      const binaryString = e.target.result;
      const workbook = XLSX.read(binaryString, { type: 'binary' });
      const firstSheetName = workbook.SheetNames[0];
      const worksheet = workbook.Sheets[firstSheetName];
  
      // Convert worksheet data to a nested header structure
      this.excelData = this.convertSheetData(worksheet);
      // console.log(this.excelData);

      let flag: boolean = false;

      const secondColumnValues: any[] = this.data.map(row => row[1]);
      secondColumnValues.push('23:45 - 24:00')
      this.tempData = [];
      
      for(var i =0; i < this.excelData.rows.length; i++) {
        if((this.excelData.rows[i][0] >= 1 && this.excelData.rows[i][0] <= 96) && secondColumnValues.includes(this.excelData.rows[i][1]) ){
          this.tempData.push(this.excelData.rows[i].slice(0,25))
        }
        
        
      }

      let totalCount = this.getTotalElements(this.tempData);

      this.loadedData = true;

      // console.log(this.tempData[0])
      // console.log(this.tempData[0].length)

      // console.log(totalCount)

        // Check if column 2 (index 1) contains all zeroes
       
// console.log(this.tempData.length,totalCount)
        if (this.tempData.length !== 96 || totalCount !== 96 * 25) {
          // Show error message if data is not in proper format or totalCount is incorrect
          Swal.fire({
              text:  'The data you have uploaded is not in the proper format, Please upload based on the format provided above.',
              confirmButtonColor: 'rgb(3, 142, 220)',
          }).then(() => {
              this.validationform.get('excelFile')!.setValue(null); // Reset form control
              event.target.value = null; // Clear file input
          });
          return;
      }
      
      // Check if Forecasted Demand contains all zeroes
      let allZeroes = true;
      for (let i = 0; i < this.tempData.length; i++) {
        if (Number(this.tempData[i][2]) !== 0) { // Index 1 for second column
          allZeroes = false;
          break;
        }
      }
      
      if (allZeroes) {
          Swal.fire({
              text: 'Forecasted Demand contains all zeroes. Please correct the data.',
              confirmButtonColor: 'rgb(3, 142, 220)',
          }).then(() => {
              this.validationform.get('excelFile')!.setValue(null); // Reset form control
              event.target.value = null; // Clear file input
          });
          return;
      }
      
      // If data is valid
      Swal.fire({
          text: 'Data is successfully loaded, you can now preview the data!',
          confirmButtonColor: 'rgb(3, 142, 220)',
      });


    //   if (this.tempData.length!==0){

    //     let allZeroes = true;
    //     for (let i = 0; i < this.tempData.length; i++) {
    //       if (Number(this.tempData[i][2]) !== 0) { // Index 1 for second column
    //         allZeroes = false;
    //         break;
    //       }
    //     }

    //     if (allZeroes) {
    //       Swal.fire({
    //         text: 'Forecasted Demand contains all zeroes. Please correct the data.',
    //         confirmButtonColor: 'rgb(3, 142, 220)',
    //       }).then(() => {
    //         this.validationform.get('excelFile')!.setValue(null); // Reset form control
    //         event.target.value = null; // Clear file input
    //       });
    //       return;
    //     }


      
    //   if(totalCount == 96*25) {
    //       Swal.fire({text:'Data is successfully loaded, you can now preview the data!',confirmButtonColor: 'rgb(3, 142, 220)',});

    //   }
    // }
    //   else {
    //     Swal.fire({text:'The data you have uploaded is not in the proper format, Please upload based on the format provided above.',confirmButtonColor: 'rgb(3, 142, 220)',}).then(() => {
    //       this.validationform.get('excelFile')!.setValue(null); // Reset form control
    //       event.target.value = null; // Clear file input
    //     });   

    //   }

      this.spreadsheet.nativeElement.jexcel.setData(this.tempData);

      



      
      

      // if(this.tempData.length >= 0 && (this.tempData.length != 96 || this.tempData[0].length !=  21)) {
      //   Swal.fire({text:'The data you have uploaded is not in the proper format, Please upload based on the format provided above.',confirmButtonColor: 'rgb(3, 142, 220)',});   

        
      // }
      // else {
      //   console.log("Entered to save the data!")
      //   // this.data = this.tempData;
      //   this.spreadsheet.nativeElement.jexcel.setData(this.data);
      //   Swal.fire({text:'Data is successfully loaded, you can now preview the data!',confirmButtonColor: 'rgb(3, 142, 220)',});


      // }
      
  
      // console.log(this.data);
      // this.ngAfterViewInit();
  
      // const x = this.spreadsheet.nativeElement;
      // console.log(x);
      // x.innerHTML = '';
  
  
      
  
      // this.ngAfterViewInit();
  
      // Swal.fire({text:'Data is successfully loaded, you can now preview the data!',confirmButtonColor: 'rgb(3, 142, 220)',});

      
  
  
  
      // this.previewClicked = true;
      
      
      
      
    };
    reader.readAsBinaryString(file);
  }

  getTotalElements(arr: any[][]): number {
    let totalCount = 0;
  
    for (const row of arr) {
      totalCount += row.length;
    }
  
    return totalCount;
  }
  
  convertSheetData(worksheet: XLSX.WorkSheet): { header: any[]; rows: any[] } {
    const data: any[] = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
    const headerRow = data[0];
    const headerMap = new Map<number, any>();
    
    // console.log(headerRow);
    // console.log("After headerRow day ahead")
    // Map headers to their respective columns
    headerRow.forEach((header: any, index: any) => {
      if (!headerMap.has(index)) {
        headerMap.set(index, []);
      }
      headerMap.get(index).push(header);
    });
  
    const header: any[] = Array.from(headerMap.values()).map((headers: any[]) => {
      return headers.length > 1
        ? { text: headers[0], colspan: headers.length }
        : { text: headers[0], colspan: 1 };
    });
  
    const rows = data.slice(1);
  
    return { header, rows };
  }
  
  
  
  
  
  
  
   
  
  }
  








/**
 * Fetches the data
 */


/***
* Calender Set
*/


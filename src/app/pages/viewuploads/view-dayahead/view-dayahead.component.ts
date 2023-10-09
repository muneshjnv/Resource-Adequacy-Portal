import { Component } from '@angular/core';

@Component({
  selector: 'app-view-dayahead',
  templateUrl: './view-dayahead.component.html',
  styleUrls: ['./view-dayahead.component.scss']
})
export class ViewDayaheadComponent {

  breadCrumbItems!: Array<{}>;


  ngOnInit(): void {
    this.breadCrumbItems = [
      { label: 'Past Uploads' },
      { label: 'Day Ahead Forecast', active: true }
    ];

  }

}

import { Component } from '@angular/core';

@Component({
  selector: 'app-yearahead',
  templateUrl: './yearahead.component.html',
  styleUrls: ['./yearahead.component.scss']
})
export class YearaheadComponent {

  breadCrumbItems!: Array<{}>;


  ngOnInit(): void {

    this.breadCrumbItems = [
      { label: 'File Uploads' },
      { label: 'Month Ahead Forecast', active: true }
    ];

  }

}

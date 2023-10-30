import { Component } from '@angular/core';

@Component({
  selector: 'app-monthahead',
  templateUrl: './monthahead.component.html',
  styleUrls: ['./monthahead.component.scss']
})
export class MonthaheadComponent {

  breadCrumbItems!: Array<{}>;

  ngOnInit(): void {

    this.breadCrumbItems = [
      { label: 'File Uploads' },
      { label: 'Month Ahead Forecast', active: true }
    ];

  }


}

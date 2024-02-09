import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { api_url } from '../helpers/urlentry';

@Injectable({
  providedIn: 'root'
})
export class YearAheadForecastService {

  url = api_url;

  constructor(public http: HttpClient) { }

  fetchFormat() {
    return this.http.get<any>(this.url + '/yearaheadformat')
  }


  uploadYearAheadFile(formData: any) {
    return this.http.post<any>(this.url + '/uploadyearahead', formData)
  }
}

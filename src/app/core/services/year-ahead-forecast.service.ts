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

  fetchRevisions(state: any, from_date: any, to_date: any) {
    return this.http.post<any>(this.url + '/fetchyearrevisions', {"state": state, "from_date": from_date, "to_date": to_date})
  }

  
  fetchRevisionsData(state: any, from_date: any, to_date: any, revision: any) {
    return this.http.post<any>(this.url + '/fetchyearlyrevisionsdata', {"state": state, "from_date": from_date, "to_date": to_date, "revision": revision})
  }
}

import { Injectable } from '@angular/core';
import { api_url } from '../helpers/urlentry';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class MonthAheadForecastService {

  url = api_url;

  constructor(private http: HttpClient) { }



  fetchFormat() {
    return this.http.get<any>(this.url + '/monthaheadformat')
  }

  uploadWeekAheadFile(formData: any) {
    return this.http.post<any>(this.url + '/uploadmonthahead', formData)
  }

  fetchRevisions(state: any, from_date: any, to_date: any) {
    return this.http.post<any>(this.url + '/fetchmonthrevisions', {"state": state, "from_date": from_date, "to_date": to_date})
  }

  
  fetchRevisionsData(state: any, from_date: any, to_date: any, revision: any) {
    return this.http.post<any>(this.url + '/fetchmonthlyrevisionsdata', {"state": state, "from_date": from_date, "to_date": to_date, "revision": revision})
  }
}

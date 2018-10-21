import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { HealthCareRecordComponent } from './health-care-record.component';

describe('HealthCareRecordComponent', () => {
  let component: HealthCareRecordComponent;
  let fixture: ComponentFixture<HealthCareRecordComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ HealthCareRecordComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(HealthCareRecordComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

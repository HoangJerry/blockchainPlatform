import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SiderbarLeftComponent } from './siderbar-left.component';

describe('SiderbarLeftComponent', () => {
  let component: SiderbarLeftComponent;
  let fixture: ComponentFixture<SiderbarLeftComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SiderbarLeftComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SiderbarLeftComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

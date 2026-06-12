import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    filters,
    ContextTypes,
)

# ── تنظیمات ─────────────────────────────────────
TELEGRAM_TOKEN = "8649086732:AAFiCn_FZQz_vJR-Khz_9X1_KIpwYR6Qnw8"
GEMINI_API_KEY = "AQ.Ab8RN6LgVVY2hBnAzSQFAjCyaVJAVQAw2F_xUfQw4WRn9U-NAQ"
SUPPORT_USERNAME = "@your_support_username"
# ────────────────────────────────────────────────

logging.basicConfig(level=logging.INFO)

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

KNOWLEDGE_BASE = """
تو دستیار مجازی آسیاطب هستی. اطلاعات زیر رو داری و بر اساس اونا جواب میدی.
فقط بر اساس همین اطلاعات جواب بده. اگه سوال ربطی به این موضوعات نداشت، بگو که
این موضوع خارج از حوزه مشاوره آسیاطب است و کاربر رو به پشتیبان راهنمایی کن.
هیچوقت توصیه پزشکی قطعی نده و همیشه در انتها بگو برای درمان قطعی با متخصص مشورت کن.
جواب‌هایت رو به فارسی بده.

=== اطلاعات آسیاطب ===

موضوع ۱: اختلال نعوظ / شلی آلت / بلند نشدن / سفت نشدن

روش اول - دوره درمانی:
- مدت: ۱ ماه، روزانه
- مکمل‌های گیاهی پایه (جنسینگ، موکا، آووکادو، یوهنبین، آرژنین)
- مصرف: ۱ کپسول بعد از نهار + ۱ کپسول بعد از شام
- نتیجه: سفتی و نعوظ کامل بعد از اتمام دوره
- از هفته اول تغییرات پله‌پله احساس می‌شود
- بعد از دوره تا ۶ ماه نیاز به دارو نیست
- مزایا: کاملاً گیاهی، بدون عوارض

روش دوم - مقطعی (قبل از رابطه):
- نصف قرص با آب فراوان، ۱۵ تا ۳۰ دقیقه قبل از رابطه
- نتیجه: سفتی کامل بعد از ۳۰ دقیقه
- عوارض احتمالی: سردرد در بعضی افراد (به دلیل ترکیبات شیمیایی کنترل‌شده)

موضوع ۲: انزال زودرس / زود تموم شدن / دیر نیومدن

روش اول - دوره درمانی:
- مدت: ۱ ماه، روزانه
- مکمل‌های گیاهی پایه
- مصرف: ۱ کپسول بعد از نهار + ۱ کپسول بعد از شام
- نتیجه: تأخیر حداقل ۱۵ دقیقه‌ای به صورت مداوم
- اثر تا ۶ ماه بعد از دوره باقی می‌ماند
- از هفته اول تغییرات احساس می‌شود

روش دوم - مقطعی (قبل از رابطه):
- نصف قرص با آب فراوان، ۱۵ تا ۳۰ دقیقه قبل از رابطه
- نتیجه: تأخیر تا ۳۰ دقیقه علاوه بر تأخیر طبیعی فرد
- عوارض احتمالی: سردرد در بعضی افراد

موضوع ۳: تقویت برای روابط مکرر / چند بار در روز / استقامت

روش: ترکیب دوره درمانی و مقطعی
- روزانه ۱ کپسول بعد از عصرانه
- ربع قرص قبل از هر رابطه
- نتیجه: نعوظ کامل + تأخیر ۳۰ دقیقه‌ای

موضوع ۴: تغییر سایز / بزرگ‌تر شدن / پیرونی / انحراف آلت

روش: دوره درمانی ۹۰ روزه
- دستگاه وکیوم + کرم و ژل و روغن گیاهی

طریقه استفاده از دستگاه وکیوم:
- روزانه ۱۵ دقیقه
- آلت را داخل محفظه شیشه‌ای قرار دهید
- با تلمبه عمل مکش انجام دهید تا آلت تحت فشار قرار گیرد
- ۱۵ ثانیه تحت فشار نگه دارید
- با سوپاپ هوا را خارج کنید
- ۱۰ ثانیه استراحت
- این عمل را تکرار کنید تا ۱۵ دقیقه کامل شود

طریقه استفاده از کرم/ژل/روغن:
- یک بند انگشت از محصول را دور بدنه آلت بزنید
- ۱ دقیقه ماساژ دهید
- ۵ دقیقه استراحت
- بشویید

نتیجه بعد از ۹۰ روز:
- افزایش ۳ تا ۵ سانتی‌متر در طول
- افزایش ۲ تا ۳ سانتی‌متر در قطر
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! 👋 به آسیاطب خوش اومدی.\n\n"
        "هر سوالی درباره مشکلات جنسی داری بپرس، راهنماییت می‌کنم. 🌿\n\n"
        f"در صورت نیاز به مشاوره تخصصی‌تر: {SUPPORT_USERNAME}"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    
    await update.message.reply_text("در حال بررسی... ⏳")
    
    try:
        prompt = f"{KNOWLEDGE_BASE}\n\nسوال کاربر: {user_message}\n\nجواب:"
        response = model.generate_content(prompt)
        answer = response.text
        
        await update.message.reply_text(answer)
        
    except Exception as e:
        await update.message.reply_text(
            "متأسفم، مشکلی پیش اومد. لطفاً دوباره امتحان کن یا با پشتیبان تماس بگیر.\n"
            f"{SUPPORT_USERNAME}"
        )

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("ربات آسیاطب (نسخه هوشمند) در حال اجراست...")
    app.run_polling()

if __name__ == "__main__":
    main()
